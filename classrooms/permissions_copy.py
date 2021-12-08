from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Classroom
from institutions.models import Staff
from django.shortcuts import get_object_or_404
from subscriptions.models import ClassroomSubscription


class IsClassroomCreator(BasePermission):
    message = "Editing posts is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user
