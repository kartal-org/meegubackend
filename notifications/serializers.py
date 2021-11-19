from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
