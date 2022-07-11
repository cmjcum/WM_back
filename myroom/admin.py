from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Furniture)
admin.site.register(models.MyFurniture)
admin.site.register(models.FurniturePosition)