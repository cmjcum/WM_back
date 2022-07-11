from django.contrib import admin
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel


# Register your models here.
admin.site.register(UserModel)
admin.site.register(UserInfoModel)
admin.site.register(ArticleLikeModel)
admin.site.register(PlanetModel)