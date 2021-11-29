from rest_framework import serializers
from .models import *
from users.models import NewUser


class InstitutionSerializer(serializers.ModelSerializer):
    # owner = serializers.CharField(source="owner.full_name", read_only=True)

    class Meta:
        model = Institution
        fields = "__all__"
        # extra_kwargs = {"owner": {"read_only": True}}


class InstitutionByStaffSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ["institution"]


class StaffInstitutionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="institution.id")
    name = serializers.CharField(source="institution.name")

    class Meta:
        model = Staff
        fields = ["id", "name"]


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
    name = serializers.CharField(source="user.full_name", read_only=True)
    image = serializers.FileField(source="user.image", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}, "user": {"read_only": True}}


class StaffTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffType
        fields = "__all__"
