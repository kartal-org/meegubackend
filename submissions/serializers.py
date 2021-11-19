from django.db.models import fields
from rest_framework import serializers
from .models import *


class ClassroomSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomSubmission
        fields = "__all__"
