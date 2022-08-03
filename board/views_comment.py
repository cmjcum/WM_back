from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CommentPostSerializer
from .models import Comment as CommentModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel

def is_okay(request, planet_id):
    user = request.user

    if user.is_authenticated:

        if user.is_admin:
            return True
    
        if planet_id == PlanetModel.objects.get(name="Solar").id:
            return True
        
        if planet_id == UserInfoModel.objects.get(user__id=user.id).planet.id:
            return True

    return False


# 댓글 CRUD
class CommentView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
        
    def post(self, request, planet_id, article_id):
        '''
        댓글을 작성합니다.
        '''
        if is_okay(request, planet_id):
            user = request.user.id

            data = request.data.copy()
            data['author'] = user
            data['article'] = article_id

            comment_serializer = CommentPostSerializer(data=data)

            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"detail":"권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 수정합니다.
        '''
        if is_okay(request, planet_id):

            user = request.user.id
            comment = CommentModel.objects.get(id=reply_id)
            
            if user == comment.author.id: # 게시글 작성자가 맞는지 확인
                comment_serializer = CommentPostSerializer(comment, data=request.data, partial=True)

                if comment_serializer.is_valid():
                    comment_serializer.save()
                    return Response(comment_serializer.data, status=status.HTTP_200_OK) 

                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, planet_id, article_id, reply_id):
        '''
        댓글을 삭제합니다.
        '''
        if is_okay(request, planet_id):

            user = request.user.id
            comment = CommentModel.objects.get(id=reply_id)
        
            if user == comment.author.id: # 게시글 작성자가 맞는지 확인
                comment.delete()
                return Response({'message': '삭제 완료!'}, status=status.HTTP_200_OK)       
 
            return Response({'detail': '이 글을 작성한 사람이 아닙니다!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail":"권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)