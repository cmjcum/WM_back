import django
django.setup()

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView

from datetime import datetime
from multiprocessing import Process
import imageio

from .serializers import PlanetLogSerializer, PlanetSerializer, UserInfoSerializer
from .serializers import PlanetLog
from user.serializers import UserSerializer
from user.jwt_claim_serializer import CustomTokenObtainPairSerializer

from .models import Planet, PlanetLog
from .models import UserInfo

from makemigrations.permissions import HasNoUserInfoUser, HasNoRoom

from deeplearning.deeplearning_make_portrait import make_portrait


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response({"message": "회원가입 완료"}, status=status.HTTP_200_OK)
                
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [HasNoUserInfoUser]
    
    def post(self, request):

        request.data['user'] = request.user.id
        pic = imageio.imread(request.data.pop('portrait')[0])

        user_info_serializer = UserInfoSerializer(data=request.data)
        if user_info_serializer.is_valid():
            user_info_serializer.save()

            p = Process(target=make_portrait, args=(pic, request.user.id))
            p.start()

            return Response(status=status.HTTP_200_OK)

        return Response(user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PutPortraitView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, owner_id):
        if request.user.id == owner_id:

            pic = imageio.imread(request.data.pop('portrait')[0])
            p = Process(target=make_portrait, args=(pic, request.user.id))
            p.start()

            return Response({'message': '프로필 수정 완료!'})
            
        return Response({'message': '프로필 수정 실패'}, status=status.HTTP_400_BAD_REQUEST)


class PlanetView(APIView):
    permission_classes = [HasNoRoom]

    def get(self, request):
        planets = Planet.objects.all()
        planet_serializer = PlanetSerializer(planets, many=True).data
        
        return Response(planet_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        planet_name = data.pop('planet')
        planet_id = Planet.objects.get(name=planet_name).id

        data['planet'] = planet_id

        planet_log_serializer = PlanetLogSerializer(data=data)
        if planet_log_serializer.is_valid():
            planet_log_serializer.save()
        else:
            return Response(planet_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now()
        date = now.strftime('%m%d')
        data['identification_number'] = f'{planet_id}{date}{request.user.id}'
        user_info = UserInfo.objects.get(user=request.user)

        user_info_serializer = UserInfoSerializer(user_info, data=data, partial=True)
        if user_info_serializer.is_valid():
            user_info_serializer.save()

            PlanetLog.objects.filter(planet=data['planet'], floor=data['floor'], room_number=data['room_number']).delete()
            return Response(status=status.HTTP_200_OK)

        PlanetLog.objects.filter(planet=data['planet'], floor=data['floor'], room_number=data['room_number']).delete()
        return Response(user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)