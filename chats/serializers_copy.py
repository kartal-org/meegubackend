from rest_framework import serializers
from .models_copy import *
from users.models import NewUser


class ChatRoomSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(slug_field="username", many=True, queryset=NewUser.objects.all())

    class Meta:
        model = ChatRoom
        fields = ["id", "name", "members", "latest_message", "code"]


class UserChatSerializer(serializers.ModelSerializer):
    profileImage = serializers.FileField()

    class Meta:
        model = NewUser
        fields = ["id", "username", "full_name", "profileImage"]


class ChatRoomGetMembersSerializer(serializers.ModelSerializer):
    members = UserChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ["id", "members"]


class ChatMessageSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(slug_field="code", queryset=ChatRoom.objects.all())

    class Meta:
        model = ChatMessage
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["sender"] = UserChatSerializer(instance.sender).data
        return response
