from django.db import models


# 가구
class Furniture(models.Model):
    name = models.CharField(max_length=15)
    width = models.IntegerField()
    height = models.IntegerField()
    url_left = models.URLField()
    url_right = models.URLField()
    price = models.IntegerField()


# 나의 가구
class MyFurniture(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)


# 가구 위치
class FurniturePosition(models.Model):
    myfurniture = models.ForeignKey(MyFurniture, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    is_left = models.BooleanField(default=True)


# 방명록
class GuestBook(models.Model):
    author = models.ForeignKey('user.User', related_name='author_set', on_delete=models.CASCADE)
    owner = models.ForeignKey('user.User', related_name='owner_set', on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)