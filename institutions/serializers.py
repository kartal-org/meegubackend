# from rest_framework import serializers
# from .models import *
# from users.models import NewUser


# class InstitutionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Institution
#         fields = "__all__"
#         extra_kwargs = {"owner": {"read_only": True}}


# class ModifiedInstitutionSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source="institution.name")
#     description = serializers.CharField(source="institution.description")
#     id = serializers.CharField(source="institution.id")
#     cover = serializers.FileField(source="institution.cover")

#     class Meta:
#         model = InstitutionVerification
#         fields = [
#             "name",
#             "description",
#             "id",
#             "cover",
#             "status",
#         ]

#     pass


# class InstitutionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Institution
#         fields = "__all__"


# class CreateInstitutionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Institution
#         fields = ("id", "name", "description")


# class InstitutionVerificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstitutionVerification
#         fields = "__all__"


# class InstitutionSubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InstitutionSubscription
#         fields = "__all__"
