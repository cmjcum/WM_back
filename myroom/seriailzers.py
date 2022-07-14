from rest_framework import serializers

from myroom.models import Furniture as FurnitureModel
from myroom.models import MyFurniture as MyFurnitureModel
from myroom.models import FurniturePosition as FurniturePositionModel
from myroom.models import GuestBook as GuestBookModel



from user.models import UserManager as UserManagerModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel


class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel
        fields = ["name", "birthday", "portrait", "coin"]


class RoomDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel
        fields = ["name" "portrait"]


class PostGuestBookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestBookModel
        fields = ["content","author", "owner"]


class GetGuestBookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestBookModel
        fields = ["content"]