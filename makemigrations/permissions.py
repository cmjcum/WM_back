from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from user.models import UserInfo


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class HasNoUserInfoUser(BasePermission):

    message = '이주가 완료되지 않은 유저만 접근할 수 있는 페이지입니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if UserInfo.objects.filter(user__id=user.id):
            return False
        
        return True