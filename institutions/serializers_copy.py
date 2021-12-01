from rest_framework import serializers
from .models import *
from users.models import NewUser


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "cover",
            "privacy",
            "storage_left",
            "is_Verified",
            "storage_used",
        ]


class InstitutionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class InstitutionListSerializer(serializers.ModelSerializer):
    institutions = InstitutionFieldSerializer(read_only=True, many=True)

    class Meta:
        model = Staff
        fields = ["institutions"]


class StaffSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name")

    class Meta:
        model = Staff
        fields = "__all__"


# class InstitutionVerificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstitutionVerification
#         fields = "__all__"
#         extra_kwargs = {"institution": {"read_only": True}, "status": {"read_only": True}}


# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = "__all__"
#         extra_kwargs = {"institution": {"read_only": True}}


# class StaffSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source="user.full_name", read_only=True)
#     image = serializers.FileField(source="user.image", read_only=True)
#     username = serializers.CharField(source="user.username", read_only=True)

#     class Meta:
#         model = Staff
#         fields = "__all__"
#         extra_kwargs = {"institution": {"read_only": True}, "user": {"read_only": True}}


# class StaffTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StaffType
#         fields = "__all__"
