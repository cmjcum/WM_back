from rest_framework import serializers
from django.utils import timezone, dateformat

from .models import Article as ArticleModel
from .models import Comment as CommentModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel
from user.models import ArticleLike as ArticleLikeModel
from user.models import Planet as PlanetModel

import boto3


class ArticleSerializer(serializers.ModelSerializer):
    
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
        fields = "__all__"
        #   fields = ["fieldname"]


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    article = serializers.SlugRelatedField(queryset=ArticleModel.objects.all(), slug_field='title')

    def get_reply(self, instance):
        # recursive
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

    class Meta:
        model = CommentModel
        fields = ('id', 'author', 'article', 'parent', 'content', 'reply')
        # fields = "__all__"
        #   fields = ["fieldname"]
        