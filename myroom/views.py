from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from myroom.seriailzers import UserInfoModelSerializer
from myroom.seriailzers import RoomDataSerializer
from myroom.seriailzers import PostGuestBookModelSerializer
from myroom.seriailzers import GetGuestBookModelSerializer

from myroom.models import GuestBook as GuestBookModel

from user.models import UserInfo as UserInfoModel

# permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
# permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
# permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # DONE 로그인한 user의 정보 / 방문한 마이룸의 정보
    def get(self, request, owner_id):
        user = UserInfoModel.objects.filter(user__id=owner_id)
        owner = UserInfoModel.objects.all()
        # owner = UserInfoModel.objects.filter(id=owner_id)

        if request.user.id == owner_id:
            profile_data = UserInfoModelSerializer(user, many=True).data
            return Response(profile_data, status=status.HTTP_200_OK)
        else:
            room_profile_data = RoomDataSerializer(owner, many=True).data
            return Response(room_profile_data, status=status.HTTP_200_OK)


class GuestBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # DONE 방명록 조회
    def get(self, request, owner_id):
        # __ 는 참조하고 있는 테이블의 필드를 가져온다.(__연결고리)
        guest_book = GuestBookModel.objects.filter(owner__id=owner_id)
        serializer_guest_book = GetGuestBookModelSerializer(guest_book, many=True).data
        return Response(serializer_guest_book, status=status.HTTP_200_OK)

    # DONE 방명록 작성
    def post(self, request, owner_id):
        request.data['author'] = request.user.id
        request.data['owner'] = owner_id

        serializer_guest_book = PostGuestBookModelSerializer(data=request.data)
        
        if serializer_guest_book.is_valid():
            serializer_guest_book.save()
            return Response({'message': '방명록 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)

    # TODO 방명록 삭제
    def delete(self, request, owner_id, guest_book_id):
        guest_book_list = GuestBookModel.objects.filter(owner_id=owner_id)
        guest_book = guest_book_list.objects.filter(guest_book_id=guest_book_id)
        guest_book.delete()

        return Response({'message': '방명록이 삭제되었습니다.'})

        # 첫 번째 삭제
        # guest_book = GuestBookModel.objects.filter(author=request.user, owner=owner_id).first()
        # guest_book = GuestBookModel.objects.filter(author=request.user).first()
        # guest_book = GuestBookModel.objects.filter(owner=owner_id).first()
        # 전부 삭제
        # guest_book = GuestBookModel.objects.all()
        # guest_book = GuestBookModel.objects.filter(owner_id=owner_id)
        # 처음 한번만 삭제?
        # guest_book = GuestBookModel.objects.get(id=owner_id)

