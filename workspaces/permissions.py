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


class IsOwner(BasePermission):
    message = "Editing posts is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


def checkOwner(classroom, user):
    return get_object_or_404(Classroom, pk=classroom).owner == user


class IsAdviser(BasePermission):
    message = "Creating workspaces is restricted to the adviser only."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if "WorkspaceList" in str(view):
            if checkOwner(view.kwargs.get("classroom"), user):
                return True
        if "WorkspaceDetail" in str(view):
            workspaceClassroom = get_object_or_404(Workspace, pk=view.kwargs.get("pk")).classroom.id
            if checkOwner(workspaceClassroom, user):
                return True
        return False


def checkStudent(classroom, user):
    try:
        student = Member.objects.get(user=user, classroom=classroom)
    except ObjectDoesNotExist:

        return False
    return student


class IsStudent(BasePermission):
    message = "Creating workspace folder is restricted to the student only."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if "WorkspaceFolderList" in str(view):

            workspaceClassroom = get_object_or_404(Workspace, pk=view.kwargs.get("workspace")).classroom.id
            if checkStudent(workspaceClassroom, user):
                return True
        if "WorkspaceFolderDetail" in str(view):
            workspaceClassroom = get_object_or_404(WorkspaceFolder, pk=view.kwargs.get("pk")).workspace.classroom.id

            if checkStudent(workspaceClassroom, user):
                return True
        if "QuillFileList" in str(view) or "UploadFileList" in str(view):

            workspaceClassroom = get_object_or_404(WorkspaceFolder, pk=view.kwargs.get("folder")).workspace.classroom.id
            if checkStudent(workspaceClassroom, user):
                return True
        if "QuillFileDetail" in str(view):
            workspaceClassroom = get_object_or_404(
                WorkspaceQuillFile, pk=view.kwargs.get("pk")
            ).folder.workspace.classroom.id
            if checkStudent(workspaceClassroom, user):
                return True
        if "UploadFileDetail" in str(view):
            workspaceClassroom = get_object_or_404(
                WorkspaceUploadedFile, pk=view.kwargs.get("pk")
            ).folder.workspace.classroom.id
            if checkStudent(workspaceClassroom, user):
                return True

        return False


def getClassroomSize(query):
    # Please have a function to check if the query is none and return 0
    return query.annotate(filesize=Cast("size", IntegerField())).aggregate(Sum("filesize"))["filesize__sum"]


def getClassroomTotalSize(classroom, incomingFile):
    resourceFileSize = getClassroomSize(
        ClassroomResourceUploadedFile.objects.filter(folder__resource__classroom__id=classroom)
    )
    workspaceFileSize = getClassroomSize(
        WorkspaceUploadedFile.objects.filter(folder__workspace__classroom__id=classroom)
    )

    totalFileSize = incomingFile + resourceFileSize + workspaceFileSize

    subscriptionlimit = (
        ClassroomSubscription.objects.filter(classroom=classroom)
        .annotate(storage_limit=Cast(KeyTextTransform("storage", "plan__limitations"), IntegerField()))
        .aggregate(Sum("storage_limit"))["storage_limit__sum"]
    )

    return subscriptionlimit >= totalFileSize


class IsNotSubscriptionLimit(BasePermission):
    message = "Sorry the classroom storage limit is up. Please notify your adviser to make a subscription again."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if "UploadFileList" in str(view):

            # Please also count institution files if naay institution id ang classroom
            classroomInstance = get_object_or_404(WorkspaceFolder, pk=view.kwargs.get("folder")).workspace.classroom.id
            if getClassroomTotalSize(classroomInstance, int(request.data["size"])):
                return True
        return False


class IsNotAMember(BaseMember):
    message = "Sorry the user is already a member of this workspace"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if "SharedWorkspaceList" in str(view):
            # what is given? user, classroom
            # what is needed to be checked: user is not in memberlist
            memberList = Member.objects.filter(user=user, classroom=view.kwargs.get("classroom"))
            if memberList:
                return True
        return False
