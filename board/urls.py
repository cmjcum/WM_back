from django.urls import path
from . import views 

urlpatterns = [
    path('', views.BoardListView.as_view()),
    path('', views.BoardView.as_view()),
    path('<planet>/post/', views.BoardView.as_view()),
    path('', views.BoardView.as_view()),
    path('', views.BoardView.as_view()),
]