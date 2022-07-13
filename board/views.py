from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone, dateformat

from .serializers import ArticleSerializer, CommentSerializer, RecursiveSerializer
from .models import Comment as CommentModel
from .models import Article as ArticleModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel

import boto3


# 메인 화면: 이용가능한 게시판 목록 출력
class BoardListView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)


# 게시글 CRUD
class BoardView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request, planet_id):
        '''
        게시글 목록을 조회합니다. //  게시글 제목 (댓글수) (사진유무아이콘?), 작성자, 작성일 
        '''
        # user = request.user
        articles = ArticleModel.objects.filter(planet__id=planet_id).order_by('-create_date')
        print(articles)
        article_serializer = ArticleSerializer(articles, many=True).data
        # article_serializer = CommentSerializer(articles, many=True).data
        # print(article_serializer)

        return Response(article_serializer, status=status.HTTP_200_OK)
        # return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request, planet_id):
        '''
        게시글을 작성합니다.
        사진이 있을 때는 폼데이터...
        사진이 없어버리면 json..........
        '''
        print(request.data._mutable)
        user = request.user.id

        if request.data.get('pic',None) != None:
            pic = request.data.pop('pic')[0] 
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
            request.data['picture_url'] = url

        request.data._mutable = True
        request.data['author'] = user
        request.data['planet'] = planet_id
        request.data._mutable = False

        article_serializer = ArticleSerializer(data=request.data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, planet_id, article_id):
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request, planet_id, article_id):
        return Response({'message': 'delete method!!'}, status=status.HTTP_200_OK)


# 댓글 CRUD
class CommentView(APIView):
    permission_classes = [permissions.AllowAny] 

    # def get(self, request, planet_id, article_id, ):
    #     return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request, planet_id, article_id, reply_id):
        return Response({'message': 'post method!!'}, status=status.HTTP_200_OK)

    def put(self, request, planet_id, article_id, reply_id):
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request, planet_id, article_id, reply_id):
        return Response({'message': 'delete method!!'}, status=status.HTTP_200_OK)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self): 
        queryset = CommentModel.objects.filter(parent=None)
        return queryset