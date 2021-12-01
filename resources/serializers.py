from django.db.models import fields
from rest_framework import serializers
from .models import *
from classrooms.models import Classroom


class ClassroomOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["adviser"]


class ClasssroomResourceSerializer(serializers.ModelSerializer):
    adviser = ClassroomOwnerSerializer(many=False, read_only=True)

    class Meta:
        model = ClassroomResource
        fields = "__all__"
        # extra_kwargs = {"classroom": {"read_only": True}, "owner": {"read_only": True}}


class ClasssroomResourceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceFolder
        fields = "__all__"
        # extra_kwargs = {"resource": {"read_only": True}}


class ClassroomResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceFile
        fields = "__all__"
        # extra_kwargs = {"folder": {"read_only": True}}


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


class InstitutionResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}
