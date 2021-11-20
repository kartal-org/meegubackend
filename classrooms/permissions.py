from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Classroom
from institutions.models import Staff
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

        if "privacy" in request.data:
            breakpoint()
            if request.data["privacy"] == "public" and ClassroomSubscription.objects.filter(
                classroom=request.kwargs.get("classroom")
            ):
                print("Catch")
                return True
            return False
        return True


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


class IsInstitutionStaff(BasePermission):
    message = "You are not part of this Institution"

    def has_permission(self, request, view):
        user = request.user

        if "institution" in request.data:
            # breakpoint()
            if Staff.objects.filter(user=user, institution=request.data["institution"]):
                return True
            return False
        return True
