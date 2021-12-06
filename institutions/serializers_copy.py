from django.db.models import fields
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
            "creator",
            "contact",
            "address",
            "website",
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
    institution = InstitutionFieldSerializer(read_only=True, many=False)

    class Meta:
        model = Staff
        fields = ["institution"]


class StaffTypeSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(source="type.name")

    class Meta:
        model = StaffType
        fields = "__all__"


class InstitutionVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionVerification
        fields = "__all__"
        # extra_kwargs = {"institution": {"read_only": True}, "status": {"read_only": True}}


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}}


class StaffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.full_name", read_only=True)
    image = serializers.FileField(source="user.profileImage", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", queryset=NewUser.objects.all())
    type = serializers.SlugRelatedField(slug_field="name", queryset=StaffType.objects.all())

    class Meta:
        model = Staff
        fields = "__all__"
        # extra_kwargs = {"institution": {"read_only": True}, "user": {"read_only": True}}


class DepartmentFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class StaffsDepartmentSerializer(serializers.ModelSerializer):
    department = DepartmentFieldSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ["id", "department"]


# class StaffTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StaffType
#         fields = "__all__"
