from django.db import models

# Create your models here.
class Furniture(models.Model):
    name = models.CharField(max_length=15)
    width = models.IntegerField()
    height = models.IntegerField()
    url_left = models.URLField()
    url_right = models.URLField()
    price = models.IntegerField(max_length=10)


class MyFurniture(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)


class FurniturePosition(models.Model):
    myfurniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()