from rest_framework import serializers
from .models import *


class LibraryItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="content.title")
    file = serializers.CharField(source="content.file")
    author = serializers.CharField(source="content.author")
    publisher = serializers.CharField(source="content.publisher")
    itemID = serializers.CharField(source="content.id")

    class Meta:
        model = LibraryItem
        fields = ["id", "title", "file", "author", "publisher", "itemID"]


class AddLibraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryItem
        fields = ["id", "content"]
