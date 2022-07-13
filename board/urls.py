from django.urls import path
from . import views 

urlpatterns = [
    path('', views.BoardListView.as_view()),
    # path('<int:planet>/form/', views.BoardView.as_view()),

    path('<int:planet_id>/', views.BoardView.as_view()),
    
    path('<int:planet_id>/post/', views.BoardView.as_view()),
    path('<int:planet_id>/edit/<int:article_id>/', views.BoardView.as_view()),
    path('<int:planet_id>/del/<int:article_id>/', views.BoardView.as_view()),

    path('<int:planet_id>/<int:article_id>/post/', views.CommentView.as_view()),
    path('<int:planet_id>/<int:article_id>/edit/<int:reply_id>/', views.CommentView.as_view()),
    path('<int:planet_id>/<int:article_id>/del/<int:reply_id>/', views.CommentView.as_view()),
]