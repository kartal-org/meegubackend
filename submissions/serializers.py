from django.db.models import fields
from rest_framework import serializers
from .models import *
from workspaces.models import WorkspaceFile


class SubmissionSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source="workspace.name", read_only=True)
    uploadfile = serializers.FileField(source="uploadfile.file", read_only=True)
    fileName = serializers.CharField(source="file.name", read_only=True)
    uploadfileName = serializers.CharField(source="uploadfile.name", read_only=True)

    class Meta:
        model = Submission
        fields = "__all__"
        extra_kwargs = {"workspace": {"read_only": True}}


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFile
        fields = ["id", "name", "file", "content"]

    pass


class SubmissionDetailSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source="workspace.name", read_only=True)
    file = SubmissionFileSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "workspace",
            "file",
            "authors",
            "id",
            "dateUpdated",
            "adviserResponse",
            "institutionResponse",
            "comment",
            "title",
        ]
