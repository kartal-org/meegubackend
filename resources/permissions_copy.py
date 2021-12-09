from rest_framework.permissions import BasePermission, SAFE_METHODS
from classrooms.models import Classroom
from django.shortcuts import get_object_or_404, get_list_or_404

# from .models import *
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from subscriptions.models import ClassroomSubscription
from .models import *
from institutions.models import Institution, Staff
from django.core.exceptions import ObjectDoesNotExist


class InstitutionResoureStorageLimit(BasePermission):
    message = "Sorry it seems you have reached your subscription limit please renew your subscription"

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        institutionLimit = InstitutionResourceFolder.objects.get(
            id=request.data.get("folder")
        ).resource.department.institution.storage_Limit
        institutionUsage = InstitutionResourceFolder.objects.get(
            id=request.data.get("folder")
        ).resource.department.institution.storage_used
        # Department.objects.get(id = 12).institution.storage_used
        size = int(request.data["size"])
        if institutionUsage + size >= institutionLimit:
            return False
        return True


class ClassroomResourceStorageLimit(BasePermission):
    message = "Sorry it seems you have reached your subscription limit please renew your subscription"

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        breakpoint()
        classroomLimit = ClassroomResourceFolder.objects.get(
            id=request.data.get("folder")
        ).resource.classroom.storage_Limit
        classroomUsage = ClassroomResourceFolder.objects.get(
            id=request.data.get("folder")
        ).resource.classroom.storage_used
        # Department.objects.get(id = 12).institution.storage_used
        size = int(request.data["size"])
        if classroomUsage + size >= classroomLimit:
            return False
        return True
