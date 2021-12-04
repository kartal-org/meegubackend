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


class SubmissionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class PublicationSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    submission = SubmissionFieldSerializer(read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    department = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Publication
        fields = [
            "id",
            "authors",
            "title",
            "submission",
            "abstract",
            "rating",
            "category",
            "authors",
            "privacy",
            "department",
            "dateModified",
            "is_featured",
        ]


class PublicationDetailSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    file = serializers.FileField(source="file.file", read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    department = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Publication
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


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
