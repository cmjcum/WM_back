from django.urls import path
from . import views 

urlpatterns = [
    path('', views.BoardListView.as_view()), # 메인 페이지

    path('<int:planet_id>/', views.BoardView.as_view()), # 게시판 목록 get
    
    path('<int:planet_id>/<int:article_id>/', views.ArticleView.as_view()), # 게시글 상세 get
    path('<int:planet_id>/post/', views.ArticleView.as_view()), # 게시글 post
    path('<int:planet_id>/edit/<int:article_id>/', views.ArticleView.as_view()), # 게시글 put
    path('<int:planet_id>/del/<int:article_id>/', views.ArticleView.as_view()), # 게시글 delete

    path('<int:planet_id>/<int:article_id>/post/', views.CommentView.as_view()), # 댓글 post
    path('<int:planet_id>/<int:article_id>/edit/<int:reply_id>/', views.CommentView.as_view()), # 댓글 put
    path('<int:planet_id>/<int:article_id>/del/<int:reply_id>/', views.CommentView.as_view()), # 댓글 delete
]