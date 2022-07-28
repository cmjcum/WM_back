from django.urls import path

from user.views import UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PlanetView
from .views import UserInfoView


urlpatterns = [
    path('', UserView.as_view()),
    path('user_info/', UserInfoView.as_view()),
    path('planet/', PlanetView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]