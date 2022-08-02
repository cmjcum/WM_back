import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserInfo


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # 생성된 토큰 가져오기
        # 사용자 지정 클레임 설정하기
        token['user_id'] = user.id
        token['username'] = user.username

        try:
            token['coin'] = user.userprofile.coin
            # print('last_login:', user.userinfo.last_date, 'today:', datetime.date.today())
            print('coin: ', token['coin'])
            token['today_pt'] = bool(user.userprofile.last_date != datetime.date.today())
            if token['today_pt']:
                user_info = UserInfo.objects.get(id=user.userprofile.id)
                print(user.userprofile.id)
                print(user_info)
                user_info.coin += 100
                print('100pt 지급!')
                user_info.save()
                token['coin'] = user_info.coin

            print('user_id:', token['user_id'], 'username:', token['username'], 'planet:', token['planet'], 'today_pt:', token['today_pt'], 'coin: ', token['coin'])

        except:
            pass

        try: 
            token['planet'] = user.userprofile.planet.id
        except ObjectDoesNotExist:
            token['planet'] = None
        
        return token