from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from myroom.seriailzers import UserInfoModelSerializer
from myroom.seriailzers import PostGuestBookModelSerializer
from myroom.seriailzers import GetGuestBookModelSerializer
from myroom.models import GuestBook as GuestBookModel
from user.models import UserInfo as UserInfoModel
from user.models import User as UserModel

from .models import MyFurniture
from .models import FurniturePosition
from .seriailzers import MyFurnitureSerializer
from .seriailzers import FurniturePositionSerializer


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # DONE 로그인한 user의 정보
    def get(self, request, owner_id):
        user_id = request.user.id
        # print(user)
        # UserInfoModel에서 user id 와 owner id 가 같은 것을 filter 해준다.
        user = UserInfoModel.objects.filter(user_id=owner_id)
        # UserInfoModelSerializer 의 정보를 변수에 담아 Response 해준다.
        profile = UserInfoModelSerializer(user, many=True)

        # boolean 코드
        if request.user:
            like_data = profile.data[0]["user"]
            like_user_id = [x['id'] for x in profile.data[0]["user"]["like"]]

            follow_data = profile.data[0]["user"]
            follow_user_id = [x['id'] for x in profile.data[0]["user"]["follow"]]
            
            follow_data["follow_user"] = bool(user_id in follow_user_id)
            like_data["like_user"] = bool(user_id in like_user_id)
            return Response(profile.data, status=status.HTTP_200_OK)


class GuestBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # DONE 방명록 조회
    def get(self, request, owner_id):
        # __ 는 참조하고 있는 테이블의 필드를 가져온다.(__연결고리)
        guest_book = GuestBookModel.objects.filter(owner_id=owner_id).order_by('-create_date')
        # GetGuestBookModelSerializer 의 값을 변수에 넣는다.
        serializer_guest_book = GetGuestBookModelSerializer(guest_book, many=True).data
        
        return Response(serializer_guest_book, status=status.HTTP_200_OK)

    # DONE 방명록 작성
    def post(self, request, owner_id):
        # 방명록 작성을 위해 방명록 작성에 사용되는 GuestBook 모델의 정보를 가져온다.
        request.data['author'] = request.user.id
        request.data['owner'] = owner_id
        # serializer 를 통해 값을 가져온다.
        serializer_guest_book = PostGuestBookModelSerializer(data=request.data)
        # serializer_guest_book 값이 유효하다면
        if serializer_guest_book.is_valid():
            # 저장한다.
            serializer_guest_book.save()
            return Response({'message': '방명록 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)

    # DONE 방명록 삭제
    def delete(self, request, guest_book_id):
        # GuestBookModel에서 id가 guest_book_id 인것을 가져온다.
        guest_book = GuestBookModel.objects.get(id=guest_book_id)
        # 모델에서 만든 author 와 로그인한 유저가 같다면
        if guest_book.author == request.user:
            # guest_book_id 를 삭제해준다.
            guest_book.delete()
            return Response({'message': '방명록이 삭제되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# DONE 좋아요
class LikeUserModelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, owner_id):
        # 로그인한 유저라면
        user = request.user 
        if user:
            # UserModel에서 id 값이 owner_id 인게 있으면 값을 가져오고 아니면 404에러
            owner = get_object_or_404(UserModel, id=owner_id)
            # article 안에 pk가 있다면 id를 찾는다.
            if owner.like.filter(id=request.user.id).exists():
                # pk 값을 remove()를 통해 지워준다.
                owner.like.remove(request.user)
                return Response({'message': '좋아요 삭제!'})
            else:
                owner.like.add(request.user)
                return Response({'message': '좋아요 추가!'})


# DONE 팔로우
class FollowUserModelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, owner_id):
        if request.user:
            follow_data = get_object_or_404(UserModel, id=owner_id)
            if follow_data.follow.filter(id=request.user.id).exists():
                follow_data.follow.remove(request.user)
                return Response({'message': '팔로우 삭제!'})
            else:
                follow_data.follow.add(request.user)
                return Response({'message': '팔로우 추가!'})


class MyFurnitureView(APIView):
    def get(self, request):
        furnitures = MyFurniture.objects.filter(user=request.user)
        my_furniture_serializer = MyFurnitureSerializer(furnitures, many=True).data
        return Response({'my_furniture': my_furniture_serializer}, status=status.HTTP_200_OK)
        
    def post(self, request):
        FurniturePosition.objects.filter(user=request.user).delete()
        furniture_positions = request.data['furniture_positions']

        for furniture_position in furniture_positions:
            if furniture_position == None:
                furniture_positions.remove(furniture_position)

        for furniture_position in furniture_positions:
            furniture_position['user'] = request.user.id

        print(furniture_positions)

        furniture_position_serializer = FurniturePositionSerializer(data=request.data['furniture_positions'], many=True)

        if furniture_position_serializer.is_valid():
            furniture_position_serializer.save()
            return Response(status=status.HTTP_200_OK)

        print(furniture_position_serializer.errors)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class MyRoomView(APIView):
    def get(self, request, owner_id):
        furniture_position_list = FurniturePosition.objects.filter(user=owner_id)
        furniture_position_serializer = FurniturePositionSerializer(furniture_position_list, many=True).data
        return Response({'furniture_positions': furniture_position_serializer}, status=status.HTTP_200_OK)
