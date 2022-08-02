from django.urls import path
from . import views_board, views_article, views_comment

urlpatterns = [
    path('', views_board.BoardListView.as_view()), # 메인 페이지

    path('<int:planet_id>/list/<int:page>/', views_board.BoardView.as_view()), # 게시판 목록 get
    path('<int:planet_id>/search/<str:keyword>/<int:page>/', views_board.BoardSearchView.as_view()), # 게시글 검색 get
    
    path('<int:planet_id>/<int:article_id>/', views_article.ArticleDetailView.as_view()), # 게시글 상세 get

    path('<int:planet_id>/post/', views_article.ArticleView.as_view()), # 게시글 post
    path('<int:planet_id>/editor/<int:article_id>/', views_article.ArticleView.as_view()), # 게시글 수정페이지 get
    path('<int:planet_id>/edit/<int:article_id>/', views_article.ArticleView.as_view()), # 게시글 put
    path('<int:planet_id>/del/<int:article_id>/', views_article.ArticleView.as_view()), # 게시글 delete

    path('<int:planet_id>/<int:article_id>/post/', views_comment.CommentView.as_view()), # 댓글 post
    path('<int:planet_id>/<int:article_id>/edit/<int:reply_id>/', views_comment.CommentView.as_view()), # 댓글 put
    path('<int:planet_id>/<int:article_id>/del/<int:reply_id>/', views_comment.CommentView.as_view()), # 댓글 delete

    path('like/<int:article_id>/', views_article.ArticleLikeControllerView.as_view()), # 게시글 좋아요 post/delete
]