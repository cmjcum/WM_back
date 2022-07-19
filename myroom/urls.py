from django.urls import path
from myroom import views


urlpatterns = [
    path('<int:owner_id>/', views.UserInfoView.as_view()),
    path('content/', views.GuestBookView.as_view()),
    path('user/<int:owner_id>/', views.GuestBookView.as_view()),
    path('book/<int:guest_book_id>/', views.GuestBookView.as_view()),
    path('like/<int:owner_id>/', views.LikeUserModelView.as_view()),
    path('follow/<int:owner_id>/', views.FollowUserModelView.as_view()),
    # //////////////////////////////////////////////////////////////////
    path('test/', views.TestView.as_view()),
    path('room/', views.MyRoomTestView.as_view()),
]