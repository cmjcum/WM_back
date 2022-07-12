from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from myroom.seriailzers import ResidentDataSerializer
from myroom.seriailzers import RoomDataSerializer
from myroom.seriailzers import GuestBookModelSerializer



class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능

    def get(self, request):
        user = request.user
        resident_data = user.filter(id=user.id)
        # request.data["user"] = request.user.id

        serializer_room_data = RoomDataSerializer(user, many=True).data
        serializer_resident_data = ResidentDataSerializer(resident_data, many=True).data

        profile_data = {
            # 주민등록증
            "resident_data" : serializer_resident_data,
            # 마이룸 정보
            "room_data" : serializer_room_data,
        }

        return Response(profile_data, status=status.HTTP_200_OK)


class GuestBookView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능

    # 방명록 조회
    def get(self, request):
        guest_book = request.content
        serializer_guest_book = GuestBookModelSerializer(guest_book, many=True).data
        return Response(serializer_guest_book, status=status.HTTP_200_OK)

    # 방명록 작성
    def post(self, request):

        serializer_guest_book = GuestBookModelSerializer(data=request.data)
        if serializer_guest_book.is_valid(raise_exception=True):
            serializer_guest_book.save()
            return Response({'message': '방명록 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'message': f'{serializer_guest_book.errors}'}, 400)

    # 방명록 삭제
    def delete(self, request):
        return Response({'message': 'delete method!!'})