import django
django.setup()

from rest_framework import serializers

from user.models import User as UserModel
from .models import Planet
from .models import UserInfo
from .models import PlanetLog


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
    population = serializers.SerializerMethodField(read_only=True)

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

    def get_population(self, obj):
        return obj.userinfo_set.all().count()

    class Meta:
        model = Planet
        fields = ['name', 'max_floor', 'max_number', 'population', 'empty_rooms']


class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'name', 'name_eng', 'birthday']


class AdditionalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['planet', 'identification_number', 'last_date', 'coin',
                'floor', 'room_number']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'planet', 'name', 'name_eng', 'birthday', 'portrait',
                'floor', 'room_number', 'identification_number', 'coin', 'last_date']


class PlanetLogSerializer(serializers.ModelSerializer):

    def validate(self, data):
        floor = data.get('floor')
        room_number = data.get('room_number')

        planet = data.get('planet')
        planet_id = planet.id
        max_floor = planet.max_floor
        max_number = planet.max_number

        if floor > max_floor:
            raise serializers.ValidationError(
                     detail={"error": "층 수를 다시 선택해주세요"},
                  )

        if room_number > max_number:
            raise serializers.ValidationError(
                     detail={"error": "방 번호를 다시 선택해주세요."},
                  )

        is_exist_planet_log = PlanetLog.objects.filter(planet__id=planet_id, floor=floor, room_number=room_number)
        is_empty_room = UserInfo.objects.filter(planet__id=planet_id, floor=floor, room_number=room_number)

        if is_exist_planet_log or is_empty_room:
            raise serializers.ValidationError(
                detail={"error": "이미 다른 사람이 선택한 방입니다."}
            )

        return data

    class Meta:
        model = PlanetLog
        fields = ['planet', 'floor', 'room_number']