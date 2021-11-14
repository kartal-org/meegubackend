from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import ClassroomSubscription
from django.shortcuts import get_list_or_404


class IsNotFirstClassroom(BasePermission):
    message = "Sorry the basic plan is for first time user only."

    def has_permission(self, request, view):
        user = request.user
        subscriptionList = get_list_or_404(ClassroomSubscription, classroom__owner=user)
        if 1 in [o.plan.id for o in subscriptionList]:
            return False
        return True
