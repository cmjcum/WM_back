from django.urls import path
from myroom import views


urlpatterns = [
    path('<int:owner_id>/', views.UserInfoView.as_view()),
    path('content/', views.GuestBookView.as_view()),
    path('user/<int:owner_id>/', views.GuestBookView.as_view()),
    path('book/<int:guest_book_id>/', views.GuestBookView.as_view()),
    path('like/<int:owner_id>/', views.LikeUserModelView.as_view()),
    path('follow/<int:owner_id>/', views.FollowUserModelView.as_view()),
    path('furniture/', views.MyFurnitureView.as_view()),
    path('room/<owner_id>/', views.MyRoomView.as_view()),
    path('shop/', views.ShopView.as_view()),
]