from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from myroom.seriailzers import ResidentDataSerializer
from myroom.seriailzers import RoomDataSerializer
from myroom.seriailzers import GuestBookModelSerializer

from myroom.models import GuestBook as GuestBookModel

from user.models import UserInfo as UserInfoModel
from user.models import User as UserModel





class UserInfoView(APIView):
    permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능

    def get(self, request, owner_id):
        # 로그인한 user의 정보 / 방문한 마이룸의 정보
        user = request.user
        owner = UserModel.objects.get(id=owner_id)
        if user == owner:
            profile_data = ResidentDataSerializer(user, many=True).data
        else:
            profile_data = ResidentDataSerializer(user, many=True).data
            profile_data = RoomDataSerializer(owner, many=True).data

        return Response(profile_data, status=status.HTTP_200_OK)


class GuestBookView(APIView):
    permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 방명록 조회
    def get(self, request):
        guest_book = GuestBookModel.objects.filter(content='')
        serializer_guest_book = GuestBookModelSerializer(guest_book, many=True).data
        return Response(serializer_guest_book, status=status.HTTP_200_OK)

    # 방명록 작성
    def post(self, request):
        serializer_guest_book = GuestBookModelSerializer(data=request.data)
        if serializer_guest_book.is_valid():
            serializer_guest_book.save()
            return Response({'message': '방명록 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'message': f'{serializer_guest_book.errors}'}, 400)

    # 방명록 삭제
    # def get(self, request):
        # return Response({'message': 'delete method!!'})