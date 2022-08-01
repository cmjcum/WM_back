from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone, dateformat
import boto3

from .serializers import ArticleSerializer
from .serializers import ArticlePostSerializer
from .models import Article as ArticleModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel


# 게시글 R
class ArticleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id, article_id):
        '''
        게시글 디테일 페이지를 표시합니다.
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)

        # 관리자일 때
        if user_data.is_admin:
            article = ArticleModel.objects.get(id=article_id)
            article_serializer = ArticleSerializer(article).data
            article_serializer["liked_this"] = bool(user in article_serializer["likes"])
            return Response(article_serializer, status=status.HTTP_200_OK)

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list:
            article = ArticleModel.objects.get(id=article_id)
            article_serializer = ArticleSerializer(article).data
            print(user, article_serializer["likes"], bool(user in article_serializer["likes"]))
            article_serializer["liked_this"] = bool(user in article_serializer["likes"])

            return Response(article_serializer, status=status.HTTP_200_OK)
        
        return Response({"detail":"조회 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 게시글 CUD
class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id, article_id):
        '''
        게시글 수정 페이지를 표시합니다.
        '''
        user = request.user.id
        article = ArticleModel.objects.get(id=article_id)

        if user == article.author.id: # 게시글 작성자가 맞는지 확인
            article_serializer = ArticleSerializer(article).data
            return Response(article_serializer, status=status.HTTP_200_OK)
        return Response({"detail":"작성 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, planet_id):
        '''
        게시글을 작성합니다.
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)

        # 관리자일 때
        if user_data.is_admin:
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

            article_serializer = ArticlePostSerializer(data=data)

            if article_serializer.is_valid():
                article_serializer.save()
                return Response(article_serializer.data, status=status.HTTP_200_OK)
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
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

            article_serializer = ArticlePostSerializer(data=data)

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

        article = ArticleModel.objects.get(id=article_id)
        author = article.author.id
        
        if user == author: # 게시글 작성자가 맞는지 확인
            article_serializer = ArticlePostSerializer(article, data=request.data, partial=True)

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
        article = ArticleModel.objects.get(id=article_id)
        author = article.author.id

        if user == author: # 게시글 작성자가 맞는지 확인
            article.delete()
            return Response({'message': '삭제 완료!'}, status=status.HTTP_200_OK)       
        return Response({'message': '이 글을 작성한 사람이 아닙니다!'}, status=status.HTTP_400_BAD_REQUEST)


# TODO doLike / undoLike
class ArticleLikeControllerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, article_id):
        '''
        좋아요 등록
        게시글 id , 로그인 유저 id
        '''
        user = UserModel.objects.get(id=request.user.id)
        article = ArticleModel.objects.get(id=article_id)
        ArticleLikeModel.objects.create(user=user, article=article)
        return Response({'message': '좋아요 등록'}, status=status.HTTP_200_OK)

    def delete(self, request, article_id):
        '''
        좋아요 삭제
        게시글 id , 로그인 유저 id
        '''
        user = UserModel.objects.get(id=request.user.id)
        article = ArticleModel.objects.get(id=article_id)
        get_data = ArticleLikeModel.objects.get(user=user, article=article)
        get_data.delete()
        return Response({'message': '좋아요 삭제'}, status=status.HTTP_200_OK)    