from django.urls import path

from user.views import UserView,CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import PlanetView
from .views import UserInfoView
from .views import PutPortraitView

urlpatterns = [
    path('', UserView.as_view()),
    path('user_info/', UserInfoView.as_view()),
    path('planet/', PlanetView.as_view()),

    path('<int:owner_id>/', PutPortraitView.as_view()),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]