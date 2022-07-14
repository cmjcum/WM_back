from django.contrib import admin
from .models import Article
from .models import Comment

class CommentInline(admin.StackedInline):
    model = Comment
    # extra = 0

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'planet', 'title', 'author',  'create_date',]
    list_display_links = ['title', ]
    list_filter = ('planet',)
    inlines = (CommentInline,)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)