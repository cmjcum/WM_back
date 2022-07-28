# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Planet(models.Model):
    name = models.CharField("행성 이름", max_length=10)
    max_floor = models.IntegerField()
    max_number = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

        
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField("사용자 이름", max_length=20, unique=True)
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    follow = models.ManyToManyField("self", blank=True)
    like = models.ManyToManyField("self", blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    planet = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=10)
    name_eng = models.CharField(max_length=30)
    birthday = models.DateField()
    portrait = models.URLField()
    floor = models.IntegerField()
    room_number = models.IntegerField()
    identification_number = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    coin = models.IntegerField()
    last_date = models.DateField()


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey("board.Article", on_delete=models.CASCADE)


class PlanetLog(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    floor = models.IntegerField()
    room_number = models.IntegerField()

