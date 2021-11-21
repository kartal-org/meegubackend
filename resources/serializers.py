from django.db.models import fields
from rest_framework import serializers
from .models import *


class ClasssroomResourceSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="classroom.owner.full_name")

    class Meta:
        model = ClassroomResource
        fields = "__all__"
        extra_kwargs = {"classroom": {"read_only": True}, "owner": {"read_only": True}}


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


class InstitutionResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResource
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}, "department": {"read_only": True}}


class InstitutionResourceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceFolder
        fields = "__all__"
        extra_kwargs = {"resource": {"read_only": True}}


class InstitutionResourceQuillFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceQuillFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}


class InstitutionResourceUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceUploadedFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}
