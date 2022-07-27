import django.urls
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone, dateformat
import boto3

from .serializers import ArticleSerializer, CommentSerializer, BoardSerialzer
from .serializers import ArticlePostSerializer, CommentPostSerializer
from .models import Article as ArticleModel
from .models import Comment as CommentModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel


# 댓글 CRUD
class CommentView(APIView): 
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, planet_id, article_id, ):
    #     return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request, planet_id, article_id):
        '''
        댓글을 작성합니다.
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
            data = request.data.copy()
            data['author'] = user
            data['article'] = article_id

            print(data)

            comment_serializer = CommentPostSerializer(data=data)

            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            
            print(comment_serializer.errors)
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"detail":"작성 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 수정합니다.
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
            comment = CommentModel.objects.get(id=reply_id)
            
            if user == comment.author.id: # 게시글 작성자가 맞는지 확인
                comment_serializer = CommentPostSerializer(comment, data=request.data, partial=True)

                if comment_serializer.is_valid():
                    comment_serializer.save()
                    return Response(comment_serializer.data, status=status.HTTP_200_OK) 

                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"수정 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 삭제합니다.
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
            try:
                comment = CommentModel.objects.get(id=reply_id)
            
                if user == comment.author.id: # 게시글 작성자가 맞는지 확인
                    comment.delete()
                    return Response({'message': '삭제 완료!'}, status=status.HTTP_200_OK)       
            except:
                return Response({'message': '존재하지 않는 글입니다!'}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response({'message': '이 글을 작성한 사람이 아닙니다!'}, status=status.HTTP_400_BAD_REQUEST)