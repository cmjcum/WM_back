from django.contrib import admin
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel
from .models import PlanetLog
from . import models


# Register your models here.
# admin.site.register(UserModel)
# admin.site.register(UserInfoModel)
admin.site.register(ArticleLikeModel)
admin.site.register(PlanetModel)
admin.site.register(PlanetLog)


@admin.register(models.User)
class UserModelAdmin(admin.ModelAdmin):

    list_display = ("username", "id", "nickname")


@admin.register(models.UserInfo)
class UserInfoModelAdmin(admin.ModelAdmin):

    list_display = ("user", "planet", "name", "coin", "create_date", "last_date")