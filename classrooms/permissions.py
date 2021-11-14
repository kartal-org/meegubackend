from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Classroom
from django.shortcuts import get_object_or_404
from subscriptions.models import ClassroomSubscription


class IsOwner(BasePermission):
    message = "Editing posts is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsClassroomAdviser(BasePermission):
    message = "Editing classroom is restricted to the owner only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsStudentTypeCreator(BasePermission):
    message = "Editing student type is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if obj.custom_Type_For is None:
            return False
        return obj.custom_Type_For.owner == request.user


class IsFileOwner(BasePermission):
    message = "Editing posts is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.folder__resource__classroom__owner == request.user


class IsClassroomPaid(BasePermission):
    message = "Making classroom public is for paid classrooms only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if request.data["privacy"]:
            print("Catch")
            if ClassroomSubscription.objects.filter(classroom=obj.pk):
                return True

        return False


class IsClassroomPublic(BasePermission):
    message = "The classroom you are trying to join is private."

    def has_permission(self, request, view):
        ques = get_object_or_404(Classroom, code=request.data["classroom"])
        print("Catch 1")
        if ques.privacy == "private":
            return False
        return True


class IsNotClassroomOwner(BasePermission):
    message = "You can't join to your own classroom"

    def has_permission(self, request, view):
        ques = get_object_or_404(Classroom, code=request.data["classroom"])
        print("Catch 2")
        if ques.owner == request.user:
            return False

        return True
