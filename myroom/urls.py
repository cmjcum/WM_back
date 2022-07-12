from django.urls import path
from myroom import views


urlpatterns = [
    path('', views.UserInfoView.as_view()),
    path('content/', views.GuestBookView.as_view()),
]