from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from user.serializers import UserSerializer

from multiprocessing import Process, Queue
import boto3

from deeplearning.deeplearning_make_portrait import make_portrait

from .serializers import PlanetSerializer
from .models import Planet


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
        
        # global q, p
        
        # user_id = request.user.id
        # request.data['user'] = user_id
        
        # pic = request.data.pop('pic')[0]
        # filename = pic.name

        # s3 = boto3.client('s3')
        # s3.put_object(
        #     ACL="public-read",
        #     Bucket="my-sparta",
        #     Body=pic,
        #     Key=filename,
        #     ContentType=pic.content_type)

        # url = f'https://my-sparta.s3.ap-northeast-2.amazonaws.com/{filename}'
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