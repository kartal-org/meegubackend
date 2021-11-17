from rest_framework import serializers
from .models import *


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"
        extra_kwargs = {"classroom": {"read_only": True}, "code": {"read_only": True}}


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFolder
        fields = "__all__"
        extra_kwargs = {"workspace": {"read_only": True}}


class QuillSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceQuillFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceUploadedFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}


class SharedWorkspaceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="workspace.name")
    description = serializers.CharField(source="workspace.description")
    id = serializers.CharField(source="workspace.id")
    cover = serializers.FileField(source="workspace.cover")

    class Meta:
        model = Member
        fields = ["id", "name", "description", "cover", "classroom"]
        extra_kwargs = {"classroom": {"read_only": True}}
