from rest_framework import serializers
from ..models.classroom_models import *


class ClasssroomResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResource
        fields = "__all__"
        extra_kwargs = {"classroom": {"read_only": True}}


class ClasssroomResourceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceFolder
        fields = "__all__"
        extra_kwargs = {"resource": {"read_only": True}}


class ClassroomResourceQuillFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceQuillFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}


class ClassroomResourceUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceUploadedFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}
