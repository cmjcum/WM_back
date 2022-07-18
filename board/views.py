from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone, dateformat
import boto3

from .serializers import ArticleSerializer
from .models import Article as ArticleModel
from .models import Comment as CommentModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel


class BoardListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''
        메인 화면
        이용가능한 게시판 목록 출력
        가입 시 solar only
        입주 완료 후 solar + my planet
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)
        solar = PlanetModel.objects.get(name="Solar")
        url = f'/board/{solar.id}/'
        board_list = {"Solar":url}

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet
            name = my_planet.name
            url = f'/board/{my_planet.id}/'
            board_list[name] = url

        except: # userinfo 존재하지 않음
            pass

        return Response(board_list, status=status.HTTP_200_OK)


# 게시글 CRUD
class BoardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, planet_id):
        '''
        게시글 목록을 조회합니다.
        '''
        user = request.user.id

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        user_data = UserModel.objects.get(id=user)
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list:
            articles = ArticleModel.objects.filter(planet__id=planet_id).order_by('-create_date')
            article_serializer = ArticleSerializer(articles, many=True).data

            return Response(article_serializer, status=status.HTTP_200_OK)
        
        return Response({"detail":"조회 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        
    def post(self, request, planet_id):
        '''
        게시글을 작성합니다.
        '''
        user = request.user.id

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        user_data = UserModel.objects.get(id=user)
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list:

            data = request.data.copy()
            data['author'] = user
            data['planet'] = planet_id

            if data.get('pic',None) != None:
                pic = data.pop('pic')[0] 
                extension = "." + pic.name.split('.')[-1] 
                todays_date = dateformat.format(timezone.now(), 'ymdHis') 
                filename = f'{user}{todays_date}{extension}'

                s3 = boto3.client('s3')
                s3.put_object(
                    ACL="public-read",
                    Bucket="mysparta84",
                    Body=pic,
                    Key=filename,
                    ContentType=pic.content_type)

                url = f'https://mysparta84.s3.ap-northeast-2.amazonaws.com/{filename}'
                data['picture_url'] = url

            article_serializer = ArticleSerializer(data=data)

            if article_serializer.is_valid():
                article_serializer.save()
                return Response(article_serializer.data, status=status.HTTP_200_OK)
            
            # print(article_serializer.errors)
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"detail":"작성 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, planet_id, article_id):
        '''
        게시글을 수정합니다.
        '''
        user = request.user.id

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        user_data = UserModel.objects.get(id=user)
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list: # 게시판 이용 권한 확인
            article = ArticleModel.objects.get(id=article_id)
            
            if user == article.author.id: # 게시글 작성자가 맞는지 확인
                article_serializer = ArticleSerializer(article, data=request.data, partial=True)

                if article_serializer.is_valid():
                    article_serializer.save()
                    return Response(article_serializer.data, status=status.HTTP_200_OK) 

                return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"수정 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, planet_id, article_id):
        '''
        게시글을 삭제합니다.
        '''
        user = request.user.id

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        user_data = UserModel.objects.get(id=user)
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list: # 게시판 이용 권한 확인
            article = ArticleModel.objects.get(id=article_id)
            
            if user == article.author.id: # 게시글 작성자가 맞는지 확인
                article.delete()
                return Response({'message': '삭제 완료!'}, status=status.HTTP_200_OK)
            
        return Response({'message': '이 글을 작성한 사람이 아닙니다!'}, status=status.HTTP_400_BAD_REQUEST)


# 댓글 CRUD
class CommentView(APIView): 
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, planet_id, article_id, ):
    #     return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 작성합니다.
        '''
        return Response({'message': 'post method!!'}, status=status.HTTP_200_OK)

    def put(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 수정합니다.
        '''
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 삭제합니다.
        '''
        return Response({'message': 'delete method!!'}, status=status.HTTP_200_OK)