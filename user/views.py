from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from user.serializers import UserSerializer

from multiprocessing import Process, Queue
import boto3

from deeplearning.deeplearning_make_portrait import make_portrait

from .serializers import PlanetSerializer
from .models import Planet

from datetime import datetime

from .serializers import BasicUserInfoSerializer


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
            # make_portrait(q, url, request.user.id)
            p = Process(target=make_portrait, args=(q, url, request.user.id))
            p.start()

            return Response(status=status.HTTP_200_OK)
        # request.data['pic'] = url

        # original_pic_serializer = OriginalPicSerializer(data=request.data)

        # if original_pic_serializer.is_valid():
        #     original_pic_serializer.save()

        #     p = Process(target=make_portrait, args=(q, url, user_id))
        #     p.start()

        #     return Response({'msg': 'send'}, status=status.HTTP_200_OK)

        return Response({"error": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class PlanetView(APIView):
    def get(self, request):
        planets = Planet.objects.all()
        planet_serializer = PlanetSerializer(planets, many=True).data
        
        return Response(planet_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"error": "failed"}, status=status.HTTP_400_BAD_REQUEST)