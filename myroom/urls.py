from django.urls import path
from myroom import views


urlpatterns = [
    path('<int:owner_id>/', views.UserInfoView.as_view()),
    path('content/', views.GuestBookView.as_view()),
    path('content/<int:owner_id>/', views.GuestBookView.as_view()),
    path('content/<int:owner_id>/<int:guest_book_id>/', views.GuestBookView.as_view()),
    
    path('test/', views.TestView.as_view()),
    path('room/', views.MyRoomTestView.as_view()),
]