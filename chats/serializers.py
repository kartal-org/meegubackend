from rest_framework import serializers
from .models import *


# Revamp


# PreRevamp


class MessagesSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Conversation
        fields = ["message", "receiver"]


class PublicChatRoomSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True)

    class Meta:
        model = PublicChatRoom
        fields = ["id", "users", "messages", "title"]


class CreatePublicChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicChatRoom
        fields = ["id"]


class PublicRoomChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = PublicRoomChatMessage
        fields = ["room", "content", "user"]


class SendPublicRoomChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicRoomChatMessage
        fields = ["room", "content"]
