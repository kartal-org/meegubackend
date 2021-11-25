from rest_framework import serializers
from .models import *

# class MemberSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(many=True, read_only=True, slug_field="user__username")
#     class Meta:
#         model = Member
#         fields = "__all__"
class WorkspaceSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

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


class WorkspacMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name", read_only=True)

    username = serializers.CharField(source="user.username", read_only=True)
    image = serializers.FileField(source="user.image", read_only=True)

    class Meta:
        model = Member
        fields = "__all__"
        extra_kwargs = {"workspace": {"read_only": True}}
        # read_only_fields = ["id", "first_name", "last_name", "username", "cover"]
