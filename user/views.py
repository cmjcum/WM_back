from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from user.serializers import UserSerializer

from multiprocessing import Process, Queue
import boto3

from deeplearning.deeplearning_make_portrait import make_portrait

from .serializers import AdditionalUserInfoSerializer, PlanetLogSerializer, PlanetSerializer, UserInfoSerializer
from .models import Planet

from datetime import datetime

from .serializers import BasicUserInfoSerializer
from .serializers import PlanetLog
from .models import PlanetLog


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response({"message": "회원가입 완료"}, status=status.HTTP_200_OK)
                
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

q = Queue()
p = None
class UserInfoView(APIView):
    def post(self, request):
        global q, p
        print(q.qsize())

        request.data['user'] = request.user.id
        pic = request.data.pop('portrait')[0]

        basic_user_info_serializer = BasicUserInfoSerializer(data=request.data)
        if basic_user_info_serializer.is_valid():
            q.put(request.data)
        
            filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + pic.name
        
            s3 = boto3.client('s3')
            s3.put_object(
                ACL="public-read",
                Bucket="wm-portrait",
                Body=pic,
                Key=filename,
                ContentType=pic.content_type)

            # s3에 저장 안 하고 바로 파일 자체를 읽어서 딥페이크를 적용할 수는 없을까
            # imageio로 파일 읽는 방법?
            url = f'https://wm-portrait.s3.ap-northeast-2.amazonaws.com/{filename}'
            
            p = Process(target=make_portrait, args=(q, url, request.user.id))
            p.start()

            return Response(status=status.HTTP_200_OK)

        return Response({"error": "failed"}, status=status.HTTP_400_BAD_REQUEST)


def save_user_info(data, q):
        while q.qsize() < 2:
            pass

        basic_info = q.get()

        data['portrait'] = q.get()

        data['user'] = basic_info['user']
        data['name'] = basic_info['name']
        data['name_eng'] = basic_info['name_eng']
        data['birthday'] = basic_info['birthday']

        user_info_serializer = UserInfoSerializer(data=data)
        if user_info_serializer.is_valid():
            user_info_serializer.save()

        return


class PlanetView(APIView):
    def get(self, request):
        planets = Planet.objects.all()
        planet_serializer = PlanetSerializer(planets, many=True).data
        
        return Response(planet_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        global q
        data = request.data

        planet_name = data.pop('planet')
        planet_id = Planet.objects.get(name=planet_name).id

        planet_log = PlanetLog.objects.filter(planet=planet_id, floor=data['floor'], room_number=data['room_number'])
        data['planet'] = planet_id
        
        if not planet_log:
            planet_log_serializer = PlanetLogSerializer(data=data)
            if planet_log_serializer.is_valid():
                planet_log_serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


        now = datetime.now()
        date = now.strftime('%m%d')
        data['identification_number'] = f'{planet_id}{date}{request.user.id}'
        data['last_date'] = now.strftime('%Y-%m-%d')
        data['coin'] = 100

        additional_user_info_serializer = AdditionalUserInfoSerializer(data=data)
        if additional_user_info_serializer.is_valid():
            planet_process = Process(target=save_user_info, args=(data, q))
            planet_process.start()

            return Response(status=status.HTTP_200_OK)

        return Response({"error": "failed"}, status=status.HTTP_400_BAD_REQUEST)