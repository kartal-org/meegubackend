from rest_framework import serializers
from .models import *
from users.models import NewUser


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"


class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description"]


class JoinWorkspaceSerializer(serializers.ModelSerializer):
    workspace = serializers.SlugRelatedField(slug_field="code", queryset=Workspace.objects.all())

    class Meta:
        model = Member
        fields = ["id", "status", "workspace"]


class WorkspaceMemberSerializers(serializers.ModelSerializer):
    firstname = serializers.CharField(source="user.first_name")
    lastname = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    picture = serializers.CharField(source="user.image")

    class Meta:
        model = Member
        fields = ["id", "username", "firstname", "lastname", "picture"]


class SharedWorkspaceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="workspace.name")
    description = serializers.CharField(source="workspace.description")
    workspaceID = serializers.CharField(source="workspace.id")

    class Meta:
        model = Member
        fields = ["id", "name", "description", "workspaceID"]


class WorkspaceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFolder
        fields = "__all__"


class WorkspaceUploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceUploadedFile
        fields = "__all__"


class WorkspaceQuillFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceQuillFile
        fields = "__all__"
