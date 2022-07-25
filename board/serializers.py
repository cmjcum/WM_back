from rest_framework import serializers
from django.utils import timezone, dateformat

from .models import Article as ArticleModel
from .models import Comment as CommentModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel


class CommentSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(queryset=UserModel.objects.all(), slug_field='nickname')
    author_id = serializers.SerializerMethodField()
    article = serializers.SlugRelatedField(queryset=ArticleModel.objects.all(), slug_field='title')
    reply = serializers.SerializerMethodField()

    def get_author_id(self, obj):
        return obj.author.id

    def get_create_date(self, obj):
        try:
            return dateformat.format(obj.create_date, 'y.m.d H:i:s')

        except:
            pass

    def get_reply(self, instance):
        try:
            serializer = self.__class__(instance.comment_set, many=True)
            serializer.bind('', self)
            return serializer.data

        except:
            pass

    def validate(self, data):
        if len(data.get('content')) <= 5:
            raise serializers.ValidationError(
                detail={"error": "5글자를 넘아야 합니다."},
            )
        return data

    def create(self, validated_data):   
        comment = CommentModel(**validated_data)
        comment.save()
        return validated_data

    def update(self, instance, validated_data):
        formatted_date = dateformat.format(timezone.now(), 'y.m.d H:i')

        for key, value in validated_data.items():
            if key == 'content':
                value = value + f' ({formatted_date} 수정)'
                setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = CommentModel
        fields = [
            "id",
            "article",
            "parent",
            "author",
            "author_id",
            "content",
            "create_date",
            "reply",
        ]


class ArticleSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(queryset=UserModel.objects.all(), slug_field='nickname')
    author_id = serializers.SerializerMethodField()

    def get_author_id(self, obj):
        return obj.author.id

    def get_create_date(self, obj):
        try:
            return dateformat.format(obj.create_date, 'y.m.d H:i:s')

        except:
            pass

    def get_comments(self, obj):
        try:
            comments = obj.comment_set.filter(parent=None)
            serializer = CommentSerializer(comments, many=True)
            return serializer.data

        except:
            pass

    def validate(self, data):
        if len(data.get('content')) <= 5:
            raise serializers.ValidationError(
                detail={"error": "5글자를 넘아야 합니다."},
            )
        return data

    def create(self, validated_data):   
        article = ArticleModel(**validated_data)
        article.save()
        return validated_data

    def update(self, instance, validated_data):
        formatted_date = dateformat.format(timezone.now(), 'y.m.d H:i')

        for key, value in validated_data.items():
            if key == 'content':
                value = value + f' ({formatted_date} 수정)'
                setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = ArticleModel
        fields = [
            "id",
            "planet",
            "author",
            "author_id",
            "title",
            "content",
            "picture_url",
            "create_date",
            "comments",
        ]

class BoardSerialzer(serializers.ModelSerializer):
    # planet = serializers.SlugRelatedField(queryset=PlanetModel.objects.all(), slug_field='name')
    author = serializers.SlugRelatedField(queryset=UserModel.objects.all(), slug_field='nickname')
    create_date = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()

    def get_author_id(self, obj):
        return obj.author.id

    def get_create_date(self, obj):
        return dateformat.format(obj.create_date, 'y.m.d')

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return comments.count()

    def get_detail_url(self, obj):
        return f'article.html?board={obj.planet.id}?article={obj.id}'


    class Meta:
        model = ArticleModel
        fields = [
            "id",
            # "planet",
            "author",
            "author_id",
            "title",
            "detail_url",
            "create_date",
            "comments",
        ]