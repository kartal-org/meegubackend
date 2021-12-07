from django.db.models import fields
from rest_framework import serializers
from institutions.models import Department
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


class DepartmentFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name"]


class PublicationSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    # submission = serializers.RelatedField(required=False)
    category = CategorySerializer(read_only=True, many=True)
    institution = serializers.CharField(source="department.institution.name", read_only=True)
    archiveFile = serializers.FileField(required=False)

    class Meta:
        model = Publication
        fields = [
            "id",
            "authors",
            "title",
            "archiveFile",
            "submission",
            "institution",
            "abstract",
            "rating",
            "category",
            "authors",
            "size",
            "privacy",
            "department",
            "dateModified",
            "is_featured",
        ]
        extra_kwargs = {"submission": {"required": False}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["department"] = DepartmentFieldSerializer(instance.department).data
        return response


class PublicationDetailSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    # file = serializers.FileField(source="file.file", read_only=True)
    category = CategorySerializer(read_only=True, many=True)
    department = serializers.CharField(source="department.name", read_only=True)
    archiveFile = serializers.FileField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "authors",
            "title",
            "abstract",
            "archiveFile",
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
