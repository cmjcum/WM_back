from django.urls import path
from myroom import views


urlpatterns = [
    path('<int:owner_id>/', views.UserInfoView.as_view()),
    path('content/', views.GuestBookView.as_view()),
    path('user/<int:owner_id>/', views.GuestBookView.as_view()),
    path('book/<int:guest_book_id>/', views.GuestBookView.as_view()),
]