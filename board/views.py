from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import ArticleSerializer, CommentSerializer, RecursiveSerializer
from .models import Comment as CommentModel


# 메인 화면: 이용가능한 게시판 목록 출력
class BoardListView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)


# 게시글 CRUD
class BoardView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        return Response({'message': 'get method!!'}, status=status.HTTP_200_OK)
        
    def post(self, request):
        return Response({'message': 'post method!!'}, status=status.HTTP_200_OK)

    def put(self, request):
        return Response({'message': 'put method!!'}, status=status.HTTP_200_OK)

    def delete(self, request):
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
