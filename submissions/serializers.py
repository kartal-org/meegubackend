from django.db.models import fields
from rest_framework import serializers
from .models import *
from workspaces.models import WorkspaceFile


class WorkspaceFileFieldSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = WorkspaceFile
        fields = ["id", "name", "file", "content"]


class SubmissionSerializer(serializers.ModelSerializer):
    file = WorkspaceFileFieldSerializer(source="file.name", read_only=True)

    class Meta:
        model = Submission
        fields = ["id", "file", "title", "description", "authors", "responseStatus", "status"]


class RecommendationSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer()

    class Meta:
        model = Recommendation
        fields = ["id", "submission", "responseStatus", "department"]


class SubmissionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionResponse
        fields = "__all__"


class RecommendationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationResponse
        fields = "__all__"


# class SubmissionFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkspaceFile
#         fields = ["id", "name", "file", "content"]

#     pass


# class SubmissionDetailSerializer(serializers.ModelSerializer):
#     workspace = serializers.CharField(source="workspace.name", read_only=True)
#     file = SubmissionFileSerializer(read_only=True)

#     class Meta:
#         model = Submission
#         fields = [
#             "workspace",
#             "file",
#             "authors",
#             "id",
#             "dateUpdated",
#             "adviserResponse",
#             "institutionResponse",
#             "comment",
#             "title",
#         ]
