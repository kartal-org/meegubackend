from rest_framework import serializers

from users.models import NewUser
from .models import *
from classrooms.models import ClassroomMember


class ClassroomMemberFieldSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    userId = serializers.CharField(source="user.id", read_only=True)
    profileImage = serializers.FileField(source="user.profileImage", read_only=True)

    class Meta:
        model = ClassroomMember
        fields = ["id", "name", "username", "userId", "profileImage"]


class WorkspaceListSerializer(serializers.ModelSerializer):
    cover = serializers.FileField(read_only=True)

    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "cover", "classroom"]
        extra_kwargs = {"classroom": {"read_only": True}}


class WorkspaceForStudentListSerializer(serializers.ModelSerializer):
    # workspaces = WorkspaceListSerializer(many=True, read_only=True)
    workspace = serializers.SlugRelatedField(slug_field="code", queryset=Workspace.objects.all())
    # user = serializers.IntegerField(source="user.user.id")

    # Problem need to be solve:
    # user can be added through their username, ==> have only the user can join their selves and just filter the workspace in their
    # flattening the list

    # Joining Workspace:
    # Requirements: classroommemberID

    class Meta:
        model = Member
        fields = ["id", "workspace", "user"]
        extra_kwargs = {"user": {"read_only": True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["workspace"] = WorkspaceListSerializer(instance.workspace).data
        return response


class WorkspaceFieldSerializer(serializers.ModelSerializer):
    # serializers.SlugRelatedField()
    # members = ClassroomMemberFieldSerializer(many=True)
    cover = serializers.FileField()

    class Meta:
        model = Workspace
        fields = "__all__"
        # fields = ["id", "name", "description",  "classroom", "cover", "code"]


class StudentWorkspaceListSerializer(serializers.ModelSerializer):
    workspace = WorkspaceFieldSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ["workspace"]


class WorkspaceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFolder
        fields = "__all__"


class WorkspaceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFile
        fields = "__all__"


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    # members = MemberFieldSerializer(many=True)
    # id = serializers.CharField(source="user.id")
    # full_name = serializers.CharField(source="user.full_name")
    # username = serializers.CharField(source="user.username")
    # profileImage = serializers.FileField(source="user.profileImage")

    class Meta:
        model = Member
        fields = ["id", "user", "workspace"]
        #


class MemberFieldSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user.id")
    full_name = serializers.CharField(source="user.full_name")
    username = serializers.CharField(source="user.username")
    profileImage = serializers.FileField(source="user.profileImage")

    class Meta:
        model = ClassroomMember
        fields = ["id", "full_name", "username", "profileImage"]


class AddWorkspaceMemberSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(slug_field="user__username", queryset=ClassroomMember.objects.all())

    class Meta:
        model = Member
        fields = ["id", "workspace", "user"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = MemberFieldSerializer(instance.user).data
        return response


# extra_kwargs = {"workspace": {"read_only": True}}
# read_only_fields = ["id", "first_name", "last_name", "username", "cover"]


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
