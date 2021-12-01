from rest_framework import serializers

from users.models import NewUser
from .models import *
from classrooms.models import ClassroomMember


class ClassroomMemberFieldSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name")
    username = serializers.CharField(source="user.username")
    userId = serializers.CharField(source="user.id")
    profileImage = serializers.FileField(source="user.profileImage")

    class Meta:
        model = ClassroomMember
        fields = ["id", "name", "username", "userId", "profileImage"]


class WorkspaceSerializer(serializers.ModelSerializer):
    members = ClassroomMemberFieldSerializer(many=True, read_only=True)
    cover = serializers.FileField()

    class Meta:
        model = Workspace
        fields = "__all__"
        # fields = ["id", "name", "description", "members", "classroom", "cover", "code"]


class WorkspaceListSerializer(serializers.ModelSerializer):
    cover = serializers.FileField(read_only=True)

    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "cover", "classroom"]
        extra_kwargs = {"classroom": {"read_only": True}}


class WorkspaceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFolder
        fields = "__all__"


class WorkspaceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFile
        fields = "__all__"


# class WorkspaceSerializer(serializers.ModelSerializer):
#     # members = MemberSerializer(many=True, read_only=True)

#     class Meta:
#         model = Workspace
#         fields = "__all__"
#         extra_kwargs = {"classroom": {"read_only": True}, "code": {"read_only": True}, "creator": {"read_only": True}}

#     pass


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkspaceFile
#         fields = "__all__"
#         extra_kwargs = {"folder": {"read_only": True}}


# class NestedFileSerializer(serializers.ModelSerializer):
#     # folder = FolderSerializer()

#     class Meta:
#         model = WorkspaceFile
#         fields = "__all__"


# class QuillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WorkspaceFile
#         fields = "__all__"
#         extra_kwargs = {"folder": {"read_only": True}}


# class UploadFileSerializer(serializers.ModelSerializer):
#     # folder = FolderSerializer()

#     class Meta:
#         model = WorkspaceFile
#         fields = "__all__"
#         extra_kwargs = {"folder": {"read_only": True}}


# class SharedWorkspaceSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source="workspace.name")
#     description = serializers.CharField(source="workspace.description")
#     id = serializers.CharField(source="workspace.id")
#     cover = serializers.FileField(source="workspace.cover")

#     class Meta:
#         model = Member
#         fields = ["id", "name", "description", "cover", "classroom"]
#         extra_kwargs = {"classroom": {"read_only": True}}


# class WorkspacMemberSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source="user.full_name", read_only=True)

#     username = serializers.CharField(source="user.username", read_only=True)
#     image = serializers.FileField(source="user.image", read_only=True)
#     role = serializers.CharField(source="role.name", read_only=True)

#     class Meta:
#         model = Member
#         fields = "__all__"
#         extra_kwargs = {"workspace": {"read_only": True}}
#         # read_only_fields = ["id", "first_name", "last_name", "username", "cover"]
