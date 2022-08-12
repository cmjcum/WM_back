from django.urls import path
from . import views_board, views_article, views_comment

urlpatterns = [
    path('', views_board.BoardListView.as_view()),

    path('<int:planet_id>/list/<int:page>/', views_board.BoardView.as_view()),
    path('<int:planet_id>/search/<str:keyword>/<int:page>/', views_board.BoardSearchView.as_view()),
    
    path('<int:planet_id>/<int:article_id>/', views_article.ArticleDetailView.as_view()),

    path('<int:planet_id>/post/', views_article.ArticleView.as_view()),
    path('<int:planet_id>/editor/<int:article_id>/', views_article.ArticleView.as_view()),
    path('<int:planet_id>/edit/<int:article_id>/', views_article.ArticleView.as_view()),
    path('<int:planet_id>/del/<int:article_id>/', views_article.ArticleView.as_view()),

    path('<int:planet_id>/<int:article_id>/post/', views_comment.CommentView.as_view()),
    path('<int:planet_id>/<int:article_id>/edit/<int:reply_id>/', views_comment.CommentView.as_view()),
    path('<int:planet_id>/<int:article_id>/del/<int:reply_id>/', views_comment.CommentView.as_view()),

    path('like/<int:article_id>/', views_article.ArticleLikeControllerView.as_view()),

    path('mypage/<int:page>/', views_board.MyArticlesView.as_view()),
    path('mypage/<str:keyword>/<int:page>/', views_board.MyArticlesSearchView.as_view()),
]