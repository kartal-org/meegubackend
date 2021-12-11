from os import read
from rest_framework import serializers
from .models import *
from posts.models import Publication


class PublicationFieldSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Publication
        fields = ["id", "title", "department", "category", "publishedDate", "rating"]


class LibraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryItem
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["publication"] = PublicationFieldSerializer(instance.publication).data
        return response


# class AddLibraryItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LibraryItem
#         fields = ["id", "content"]
