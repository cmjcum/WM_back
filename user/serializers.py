from rest_framework import serializers
from user.models import User as UserModel
from .models import Planet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "password", "nickname"]

    def create(self, validated_data):

        password = validated_data.pop("password", None)
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        return user


class PlanetSerializer(serializers.ModelSerializer):
    empty_rooms = serializers.SerializerMethodField(read_only=True)

    def get_empty_rooms(self, obj):
        empty_rooms = []
        for floor in range(1, obj.max_floor+1):
            floor_rooms = []

            using_rooms = [user_info.room_number for user_info in obj.userinfo_set.filter(floor=floor)]

            for room_number in range(1, obj.max_number+1):
                if room_number not in using_rooms:
                    floor_rooms.append(room_number)
            if floor_rooms != []:
                empty_rooms.append({floor: floor_rooms})

        return empty_rooms

    class Meta:
        model = Planet
        fields = ['name', 'max_floor', 'max_number', 'empty_rooms']