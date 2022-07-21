from rest_framework import serializers

from myroom.models import GuestBook as GuestBookModel
from user.models import UserInfo as UserInfoModel

from django.utils import timezone, dateformat

from myroom.models import Furniture as FurnitureModel
from myroom.models import MyFurniture as MyFurnitureModel
from myroom.models import FurniturePosition as FurniturePositionModel
from user.models import UserManager as UserManagerModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel


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
    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, obj):
        return obj.author.nickname

    class Meta:
        model = GuestBookModel
        fields = ["content", "create_date", "nickname", "owner", "id", "author_id"]


# ////////////////////////////////////////////////////////////////////////
from .models import Furniture
from .models import MyFurniture
from .models import FurniturePosition

class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = "__all__"


class MyFurnitureSerializer(serializers.ModelSerializer):
    furniture = FurnitureSerializer()

    class Meta:
        model = MyFurniture
        fields = ['id', 'user', 'furniture']


class FurniturePositionSerializer(serializers.ModelSerializer):
    myfurniture_url = serializers.SerializerMethodField(read_only=True)

    def get_myfurniture_url(self, obj):
        if obj.is_left:
            return obj.myfurniture.furniture.url_left
        return obj.myfurniture.furniture.url_right

    class Meta:
        model = FurniturePosition
        fields = ['user', 'myfurniture', 'pos_x', 'pos_y', 'is_left', 'myfurniture_url']