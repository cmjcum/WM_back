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
        fields = "__all__"
        # fields = ["content"]


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
    # myfurniture = serializers.SerializerMethodField()

    # def get_myfurniture(self, obj):
    #     return obj.myfurniture.id

    class Meta:
        model = FurniturePosition
        fields = ['user', 'myfurniture', 'pos_x', 'pos_y', 'is_left']