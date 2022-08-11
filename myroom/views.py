from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from myroom.seriailzers import UserInfoModelSerializer
from myroom.seriailzers import PostGuestBookModelSerializer
from myroom.seriailzers import GetGuestBookModelSerializer
from .seriailzers import MyFurnitureSerializer
from .seriailzers import FurniturePositionSerializer
from .seriailzers import FurnitureSerializer
from myroom.models import GuestBook as GuestBookModel
from user.models import UserInfo as UserInfoModel
from user.models import User as UserModel
from .models import Furniture
from .models import MyFurniture
from .models import FurniturePosition
from user.models import UserInfo


from myroom.seriailzers import StatusMessageSerializer



class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, owner_id):
        user_id = request.user.id    
        user = UserInfoModel.objects.filter(user_id=owner_id)
        profile = UserInfoModelSerializer(user, many=True)
    
        if request.user:
            like_data = profile.data[0]["user"]
            like_user_id = [x['id'] for x in profile.data[0]["user"]["like"]]

            follow_data = profile.data[0]["user"]
            follow_user_id = [x['id'] for x in profile.data[0]["user"]["follow"]]
            
            follow_data["follow_user"] = bool(user_id in follow_user_id)
            like_data["like_user"] = bool(user_id in like_user_id)
            return Response(profile.data, status=status.HTTP_200_OK)

    def put(self, request, owner_id):
        user_info = UserInfoModel.objects.get(user=request.user)
        status_message = StatusMessageSerializer(user_info, data=request.data)
    
        if status_message.is_valid():        
            status_message.save()
            return Response({'message': '상메 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)


class GuestBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, owner_id):
    
        guest_book = GuestBookModel.objects.filter(owner_id=owner_id).order_by('-create_date')
    
        serializer_guest_book = GetGuestBookModelSerializer(guest_book, many=True).data
        
        return Response(serializer_guest_book, status=status.HTTP_200_OK)

    def post(self, request, owner_id):
    
        request.data['author'] = request.user.id
        request.data['owner'] = owner_id
    
        serializer_guest_book = PostGuestBookModelSerializer(data=request.data)
    
        if serializer_guest_book.is_valid():        
            serializer_guest_book.save()
            return Response({'message': '방명록 작성 완료!'})
        else:
            return Response({'message': '다시 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, guest_book_id):
    
        guest_book = GuestBookModel.objects.get(id=guest_book_id)
    
        if guest_book.author == request.user:        
            guest_book.delete()
            return Response({'message': '방명록이 삭제되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class LikeUserModelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, owner_id):
    
        user = request.user 
        if user:
            owner = get_object_or_404(UserModel, id=owner_id)
        
            if owner.like.filter(id=request.user.id).exists():
                owner.like.remove(request.user)
                return Response({'message': '좋아요 삭제!'})
            else:
                owner.like.add(request.user)
                return Response({'message': '좋아요 추가!'})


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

        furniture_position_serializer = FurniturePositionSerializer(data=request.data['furniture_positions'], many=True)

        if furniture_position_serializer.is_valid():
            furniture_position_serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class MyRoomView(APIView):
    def get(self, request, owner_id):
        furniture_position_list = FurniturePosition.objects.filter(user=owner_id)
        furniture_position_serializer = FurniturePositionSerializer(furniture_position_list, many=True).data
        return Response({'furniture_positions': furniture_position_serializer}, status=status.HTTP_200_OK)


class ShopView(APIView):
    def get(self, request):

        my_furniture_id_list = [ mf.furniture.id for mf in MyFurniture.objects.filter(user=request.user) ]
        furnitures = Furniture.objects.exclude(id__in=my_furniture_id_list)
        shop_serializer = FurnitureSerializer(furnitures, many=True).data
        coin = UserInfo.objects.get(user=request.user).coin

        return Response({'coin': coin, 'shop_serializer': shop_serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['user'] = request.user.id

        user_info = UserInfoModel.objects.get(user=request.user)
        price = Furniture.objects.get(id=request.data['furniture']).price
        coin = user_info.coin
        if coin < price:
            return Response({'flag': False, 'msg': '코인이 부족합니다!', 'coin': coin}, status=status.HTTP_200_OK)
        
        my_furniture_serializer = MyFurnitureSerializer(data=request.data)
        if my_furniture_serializer.is_valid():
            user_info.coin -= price
            user_info.save()
            my_furniture_serializer.save()

            coin = UserInfo.objects.get(user=request.user).coin
            msg = f'구매 완료! {coin} 코인 남았습니다.'

            return Response({'flag': True, 'msg': msg, 'coin': coin}, status=status.HTTP_200_OK)

        return Response(my_furniture_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
