from rest_framework import serializers
from .models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class BuySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomSubscription
        fields = "__all__"
