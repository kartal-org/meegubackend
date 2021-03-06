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
        extra_kwargs = {"classroom": {"read_only": True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["plan"] = PlanSerializer(instance.plan).data
        return response


class InstitutionSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionSubscription
        fields = "__all__"
        extra_kwargs = {"institution": {"read_only": True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["plan"] = PlanSerializer(instance.plan).data
        return response

    # class Meta:
    #     model = InstitutionSubscription
    #     fields = "__all__"
    #     extra_kwargs = {"institution": {"read_only": True}}

    #     def to_representation(self, instance):
    #         response = super().to_representation(instance)
    #         response["plan"] = PlanSerializer2(instance.plan).data
    #         return response
