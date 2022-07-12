from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import ArticleSerializer, CommentSerializer, RecursiveSerializer
from .models import Comment as CommentModel

import boto3


# 메인 화면: 이용가능한 게시판 목록 출력
class BoardListView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)


# 게시글 CRUD
class BoardView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request, planet):
        '''
        게시글 목록을 조회합니다. //  게시글 제목 (댓글수) (사진유무아이콘?), 작성자, 작성일 
        '''
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request, planet):
        '''
        게시글을 작성합니다. // 제목, 본문, 사진url 
        form data 로 받아서 이미지를 S3에 업로드하고 저장된 이미지의 url을 가졍오는 함수 필요함
        정아님꺼 긁어다 써야겠다
        
        '''
        request.data['author'] = request.user.id

        print(request.data)
        print(planet)

        # pic = request.data.pop('pic')[0]
        # filename = pic.name
        # print(filename)

        # s3 = boto3.client('s3')
        # s3.put_object(
        #     ACL="public-read",
        #     Bucket="mysparta84",
        #     Body=pic,
        #     Key=filename,
        #     ContentType=pic.content_type)

        # url = f'https://mysparta84.s3.ap-northeast-2.amazonaws.com/{filename}'
        # request.data['picture_url'] = url

        # article_serializer = ArticleSerializer(data=request.data)

        # if article_serializer.is_valid():
        #     article_serializer.save()
        #     return Response(article_serializer.data, status=status.HTTP_200_OK)

        # return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'post method!!'}, status=status.HTTP_200_OK)

    def put(self, request, planet, article):
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request, planet, article):
        return Response({'message': 'delete method!!'}, status=status.HTTP_200_OK)


# 댓글 CRUD
class CommentView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request):
        return Response({'message': 'post method!!'}, status=status.HTTP_200_OK)

    def put(self, request):
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request):
        return Response({'message': 'delete method!!'}, status=status.HTTP_200_OK)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = CommentModel.objects.filter(parent=None)
        ...
