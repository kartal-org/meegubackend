from django.db.models import fields
from rest_framework import serializers
from .models import *
from workspaces.models import Member, Workspace
from users.models import NewUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["username"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

    # class AuthorSerializer(serializers.ModelSerializer):
    #     workspace_members = serializers.SlugRelatedField(
    #         many=True, read_only=True, slug_field="id", queryset=Workspace.objects.all()
    #     )

    #     class Meta:
    #         model = Workspace
    #         fields = ["workspace_members"]

    pass


class WorkspaceForPostSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = ["members", "id", "name"]


class Article2Serializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source="file.folder.workspace.name", read_only=True)
    workspaceID = serializers.IntegerField(source="file.folder.workspace.id", read_only=True)

    # members = serializers.SlugRelatedField(slug_field="id", read_only=True)
    # members = serializers.CharField(source="file.folder.workspace.members", read_only=True)
    # authors = MemberSerializer(source="members_set")

    class Meta:
        model = Article
        fields = "__all__"

        # depth = 2
        # fields = "__all__"
        # extra_kwargs = {
        #     "institution": {"read_only": True},
        #     "slug": {"read_only": True},
        #     "workspace": {"read_only": True},
        # }


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}, "slug": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "article": {"read_only": True}}


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "article": {"read_only": True}}
