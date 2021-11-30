from django.db.models import fields
from rest_framework import serializers
from .models import *
from workspaces.models import *
from users.models import NewUser
from workspaces.serializers_copy import UploadFileSerializer


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


class Article2Serializer(serializers.ModelSerializer):
    file = UploadFileSerializer()
    # workspaceID = serializers.IntegerField(source="file.folder.workspace.id", read_only=True)

    # members = serializers.SlugRelatedField(slug_field="id", read_only=True)
    # members = serializers.CharField(source="file.folder.workspace.members", read_only=True)
    # authors = MemberSerializer(source="members_set")

    class Meta:
        model = Publication
        fields = "__all__"

        # depth = 2
        # fields = "__all__"
        # extra_kwargs = {
        #     "institution": {"read_only": True},
        #     "slug": {"read_only": True},
        #     "workspace": {"read_only": True},
        # }


class ArchiveSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source="category.name")

    class Meta:
        model = Publication
        fields = "__all__"
        extra_kwargs = {"department": {"read_only": True}, "slug": {"read_only": True}}


# class BookSerializer(serializers.ModelSerializer):
#     members = serializers.SlugRelatedField(queryset=Member.objects.all(), many=True, read_only=True,slug_field='username')

#     class Meta:
#         model = Book
#         fields = ('id', 'name', 'published', 'authors')


# class AuthorSerializer(serializers.ModelSerializer):
#     book_list = BookSerializer(many=True, read_only=True)

#     class Meta:
#         model = Author
#         fields = ('id', 'name', 'last_name', 'book_list')


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
