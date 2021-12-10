from django.db.models import fields
from rest_framework import serializers
from .models import *
from classrooms.models import Classroom
from workspaces.models import WorkspaceFile
from institutions.models import Department


class ClassroomOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["adviser"]


class ClasssroomResourceSerializer(serializers.ModelSerializer):
    adviser = ClassroomOwnerSerializer(many=False, read_only=True)

    class Meta:
        model = ClassroomResource
        fields = "__all__"
        extra_kwargs = {"adviser": {"read_only": True}}


# class ClasssroomResourceDetailSerializer(serializers.ModelSerializer):
#     adviser = ClassroomOwnerSerializer(many=False, read_only=True)

#     class Meta:
#         model = ClassroomResource
#         fields = "__all__"
#         extra_kwargs = {"adviser": {"read_only": True},}


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


class DepartmentFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class InstitutionResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResource
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["department"] = DepartmentFieldSerializer(instance.department, many=False).data
        return response


class InstitutionResourceFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceFolder
        fields = "__all__"
        # extra_kwargs = {"resource": {"read_only": True}}


class InstitutionResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionResourceFile
        fields = "__all__"
        # extra_kwargs = {"folder": {"read_only": True}}


class ImportResourceClassSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)

    class Meta:
        model = WorkspaceFile
        fields = "__all__"
        extra_kwargs = {"folder": {"read_only": True}}
