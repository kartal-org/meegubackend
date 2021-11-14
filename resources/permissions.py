from rest_framework.permissions import BasePermission, SAFE_METHODS
from classrooms.models import Classroom
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import *
from django.db.models.functions import Cast
from django.db.models import Sum, IntegerField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from subscriptions.models import ClassroomSubscription


class IsClassroomAdviser(BasePermission):
    message = "Managing Resource to the classroom is for Adviser Only"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if "ResourceListCreateView" in str(view) or "ResourceDetailView" in str(view):
            if get_object_or_404(Classroom, pk=view.kwargs.get("pk")).owner == request.user:
                return True
        if "ResourceFolderList" in str(view):
            if get_object_or_404(ClassroomResource, pk=view.kwargs.get("resource")).classroom.owner == request.user:
                return True
        if "ResourceFolderDetail" in str(view):
            if (
                get_object_or_404(ClassroomResourceFolder, pk=view.kwargs.get("pk")).resource.classroom.owner
                == request.user
            ):
                return True
        if "ResourceQuillFileList" in str(view) or "ResourceUploadFileList" in str(view):
            if (
                get_object_or_404(ClassroomResourceFolder, pk=view.kwargs.get("folder")).resource.classroom.owner
                == request.user
            ):
                return True
        if "ResourceQuillFileDetail" in str(view):
            if (
                get_object_or_404(ClassroomResourceQuillFile, pk=view.kwargs.get("pk")).folder.resource.classroom.owner
                == request.user
            ):
                return True
        if "ResourceUploadFileDetail" in str(view):
            if (
                get_object_or_404(
                    ClassroomResourceUploadedFile, pk=view.kwargs.get("pk")
                ).folder.resource.classroom.owner
                == request.user
            ):
                return True
        return False


class IsNotSubscriptionLimit(BasePermission):
    message = "Sorry it seems you have reached your subscription limit please renew your subscription"

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        fileSizeTotal = ClassroomResourceUploadedFile.objects.filter(folder=view.kwargs.get("folder")).aggregate(
            Sum("size")
        )
        combineFileSize = int(request.data["size"]) + fileSizeTotal["size__sum"]
        classroom = ClassroomResourceFolder.objects.get(pk=view.kwargs.get("folder")).resource.classroom
        limitationSize = (
            ClassroomSubscription.objects.filter(classroom=classroom)
            .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
            .aggregate(Sum("storage_limit"))
        )
        print(combineFileSize >= limitationSize["storage_limit__sum"])
        if combineFileSize >= limitationSize["storage_limit__sum"]:
            return False

        return True
