from django.db.models import fields
from rest_framework import serializers
from .models import *


class ClasssroomResourceSerializer(serializers.ModelSerializer):
    classroom = serializers.IntegerField(source="classroom.id", read_only=True)

    class Meta:
        model = ClassroomResource
        fields = ["id", "name", "description", "status", "classroom"]


class ClasssroomResourceFolderSerializer(serializers.ModelSerializer):
    resource = serializers.IntegerField(source="resource.id", read_only=True)

    class Meta:
        model = ClassroomResourceFolder
        fields = ["id", "name", "resource"]


class ClassroomResourceQuillFileSerializer(serializers.ModelSerializer):
    folder = serializers.IntegerField(source="folder.id", read_only=True)

    class Meta:
        model = ClassroomResourceQuillFile
        fields = ["id", "name", "status", "tags", "assignee", "folder", "content"]


class ClassroomResourceUploadedFileSerializer(serializers.ModelSerializer):
    folder = serializers.IntegerField(source="folder.id", read_only=True)

    class Meta:
        model = ClassroomResourceUploadedFile
        fields = ["id", "name", "status", "tags", "assignee", "folder", "file", "size"]
