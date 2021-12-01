from os import read
from rest_framework import serializers
from .models import *
from posts.models import Publication


class PublicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"


class LibraryItemSerializer(serializers.ModelSerializer):
    publication = PublicationFieldSerializer(read_only=True, many=True)

    class Meta:
        model = LibraryItem
        fields = "__all__"


# class AddLibraryItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LibraryItem
#         fields = ["id", "content"]
