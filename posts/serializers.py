from django.db.models import fields
from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {"publisher": {"read_only": True}, "slug": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "article": {"read_only": True}}


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "article": {"read_only": True}}
