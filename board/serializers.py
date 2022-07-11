from rest_framework import serializers
from .models import Article as ArticleModel
from .models import Comment as CommentModel


class ArticleSerializer(serializers.ModelSerializer):

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
        