from django.db.models import fields
from rest_framework import serializers
from .models import *


class ClassroomSubmissionSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source="workspace.name")
    file = serializers.FileField(source="")

    class Meta:
        model = ClassroomSubmission
        fields = "__all__"
        extra_kwargs = {"workspace": {"read_only": True}}
