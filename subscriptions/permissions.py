from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import ClassroomSubscription
from django.shortcuts import get_list_or_404


class IsNotFirstClassroom(BasePermission):
    message = "Sorry the basic plan is for first time user only."

    def has_permission(self, request, view):
        user = request.user
        # breakpoint()
        subscriptionList = ClassroomSubscription.objects.filter(classroom__owner=user)
        if subscriptionList:
            if "Basic Classroom" in [o.plan.name for o in subscriptionList]:
                return False
            # return True
        return True
