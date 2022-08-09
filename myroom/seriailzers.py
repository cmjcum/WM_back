from rest_framework import serializers
from django.utils import dateformat
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict

from myroom.models import GuestBook as GuestBookModel
from user.models import UserInfo as UserInfoModel
from user.models import User as UserModel
from user.models import Planet as PlanetModel
from .models import Furniture
from .models import MyFurniture
from .models import FurniturePosition


class FollowUserModelSerializer(serializers.ModelSerializer):
    follower_user_nickname = serializers.SerializerMethodField(source="nickname")
    portrait = serializers.SerializerMethodField()

    def get_follower_user_nickname(self, obj):
        return obj.nickname

    def get_portrait(self, obj):
        try:
            portrait = obj.userprofile.portrait
        except ObjectDoesNotExist:
            portrait = 'https://wm-portrait.s3.ap-northeast-2.amazonaws.com/logo/logo_ver2.png'
        return portrait

    class Meta:
        model = UserModel
        fields = ["follower_user_nickname", "id", "portrait"]


class LikeUserModelSerializer(serializers.ModelSerializer):
    like_user_nickname = serializers.SerializerMethodField(source="like")
    portrait = serializers.SerializerMethodField()

    def get_like_user_nickname(self, obj):
        return obj.nickname

    def get_portrait(self, obj):
        try:
            portrait = obj.userprofile.portrait
        except ObjectDoesNotExist:
            portrait = 'https://wm-portrait.s3.ap-northeast-2.amazonaws.com/logo/logo_ver2.png'
        return portrait

    class Meta:
        model = UserModel
        fields = ["like_user_nickname", "id", "portrait"]


class UserModelSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    follow_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    follow = FollowUserModelSerializer(many=True)
    follow_users = FollowUserModelSerializer(many=True)
    like = LikeUserModelSerializer(many=True)

    def get_like_count(self, obj):
        like_count = obj.like.count()
        return like_count

    def get_follower_count(self, obj):
        follower_count = obj.follow.count()
        return follower_count

    def get_follow_count(self, obj):
        follow_count = obj.follow_users.count()
        return follow_count

    class Meta:
        model = UserModel
        fields = ["like", "follow", "follow_users", "follower_count",
                    "follow_count", "like_count", "nickname"]


class PlanetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetModel
        fields = ["name"]


class UserInfoModelSerializer(serializers.ModelSerializer):
    birthday = serializers.SerializerMethodField()
    user = UserModelSerializer()
    planet = PlanetModelSerializer()

    def get_birthday(self, obj):
        return dateformat.format(obj.birthday, 'm.d')

    class Meta:
        model = UserInfoModel
        fields = ["name", "name_eng", "birthday", "portrait", "coin", "user_id",
                    "user", "floor", "room_number", "planet", "identification_number", "create_date"]


class RoomDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoModel
        fields = ["name" "portrait"]


class PostGuestBookModelSerializer(serializers.ModelSerializer):

    def validate(self, data):

        content_data = data.get('content')
        if '<' in data.get('content'):
            content_data = content_data.replace('<', '&lt;')
            if '>' in data.get('content'):
                data['content'] = content_data.replace('>', '&gt;')

        return data

    def create(self, validated_data):   
        article = GuestBookModel(**validated_data)
        article.save()
        return validated_data
        
    class Meta:
        model = GuestBookModel
        fields = ["content","author", "owner"]


class GetGuestBookModelSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    create_date = serializers.SerializerMethodField()

    def get_create_date(self, obj):
        return dateformat.format(obj.create_date, 'y.m.d')

    def get_nickname(self, obj):
        return obj.author.nickname

    class Meta:
        model = GuestBookModel
        fields = ["content", "create_date", "nickname", "id", "author_id"]


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = "__all__"


class MyFurnitureSerializer(serializers.ModelSerializer):

    furniture_info = serializers.SerializerMethodField(read_only=True)

    def get_furniture_info(self, obj):
        return model_to_dict(obj.furniture)

    def validate(self, data):
        user = data.get('user')
        furniture = data.get('furniture')
        is_exist = MyFurniture.objects.filter(user=user, furniture=furniture)

        if is_exist:
            raise serializers.ValidationError(
                     detail={"error": "이미 보유하고 있는 가구입니다."},
                  )

        return data

    class Meta:
        model = MyFurniture
        fields = ['id', 'user', 'furniture', 'furniture_info']


class FurniturePositionSerializer(serializers.ModelSerializer):
    myfurniture_url = serializers.SerializerMethodField(read_only=True)

    def get_myfurniture_url(self, obj):
        if obj.is_left:
            return obj.myfurniture.furniture.url_left
        return obj.myfurniture.furniture.url_right

    class Meta:
        model = FurniturePosition
        fields = ['user', 'myfurniture', 'pos_x', 'pos_y', 'is_left', 'myfurniture_url']