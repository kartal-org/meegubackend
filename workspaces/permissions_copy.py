from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404, get_list_or_404
from classrooms.models import Classroom
from subscriptions.models import ClassroomSubscription
from resources.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform


class WorkspaceFileStorageLimit(BasePermission):
    message = "Sorry the Classroom of this Workspace reached its limit."

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        # breakpoint()
        classroomLimit = WorkspaceFolder.objects.get(id=request.data.get("folder")).workspace.classroom.storage_Limit
        classroomUsage = WorkspaceFolder.objects.get(id=request.data.get("folder")).workspace.classroom.storage_used
        size = int(request.data["size"])
        if classroomUsage + size >= classroomLimit:
            return False
        return True
        # WorkspaceFolder.objects.get(id=10).workspace.classroom


class IsWorkspaceCreator(BasePermission):
    message = "Managing workspace detail is restricted to the creator only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.creator.user == request.user


class IsMemberEditPermission(BasePermission):
    message = "Managing workspace member is restricted to the creator only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.workspace.creator.user == request.user
