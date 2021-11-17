from rest_framework import serializers
from ..models.institution_models import *


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
