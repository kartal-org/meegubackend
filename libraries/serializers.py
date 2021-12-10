from os import read
from rest_framework import serializers
from .models import *
from posts.models import Publication


class PublicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"


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
