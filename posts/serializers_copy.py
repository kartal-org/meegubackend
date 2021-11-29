from django.db.models import fields
from rest_framework import serializers
from workspaces.models import *
from .models import *
from django.db.models import F


class CategorySerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Category


class ArticleListSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    # file = serializers.FileField(source="file.file")
    category = CategorySerializer(read_only=True, many=True)
    department = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "authors",
            "title",
            "file",
            "abstract",
            "category",
            "authors",
            "department",
            "dateModified",
            "is_featured",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    file = serializers.FileField(source="file.file", read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    department = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "authors",
            "title",
            "file",
            "abstract",
            "category",
            "authors",
            "department",
            "dateModified",
            "is_featured",
        ]
