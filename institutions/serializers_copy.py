from rest_framework import serializers
from .models import *
from users.models import NewUser


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"
        extra_kwargs = {"owner": {"read_only": True}}


class InstitutionVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionVerification
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}, "status": {"read_only": True}}


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}}


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}}


class StaffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffType
        fields = "__all__"
