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
    message = "Editing posts is restricted to the author only."

    def haspermission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        classroomLimit = WorkspaceFolder.objects.get(id=request.data.get("folder")).workspace.classroom.storage_Limit
        classroomUsage = WorkspaceFolder.objects.get(id=request.data.get("folder")).workspace.classroom.storage_used
        size = int(request.data["size"])
        if classroomUsage + size >= classroomLimit:
            return False
        return True
        # WorkspaceFolder.objects.get(id=10).workspace.classroom
