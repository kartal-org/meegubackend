from rest_framework.permissions import BasePermission, SAFE_METHODS
from subscriptions.models import *
from .models import Department, InstitutionVerification, Institution
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Staff, StaffType


class IsOwner(BasePermission):
    message = "Editing posts is restricted to the author only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


def isOwner(institution, user):
    return get_object_or_404(Institution, pk=institution).owner == user


def isStaff(institution, user):
    try:
        staff = Staff.objects.get(institution=institution, user=user).type.permissions["canAddPeople"]
    except ObjectDoesNotExist:
        return False
    return staff


class IsInstitutionOwner(BasePermission):
    message = "Sorry you don't have the permission to complete the action."

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if "InstitutionVerificationDetailView" in str(view):
            if get_object_or_404(InstitutionVerification, pk=view.kwargs.get("pk")).institution.owner == request.user:
                return True
        if "DepartmentListCreate" in str(view):
            if isOwner(view.kwargs.get("institution"), user):
                return True
        if "DepartmentDetail" in str(view):
            if isOwner(Department.objects.get(pk=view.kwargs.get("pk")).institution.id, user):
                return True
        if "StaffList" in str(view):
            if isOwner(view.kwargs.get("institution"), user) or isStaff(view.kwargs.get("institution"), user):
                return True
        if "StaffDetail" in str(view):
            staffInstitution = get_object_or_404(Staff, pk=view.kwargs.get("pk")).institution.id
            if isOwner(staffInstitution, user) or isStaff(staffInstitution, user):
                return True
        if "StaffTypeList" in str(view):
            if isOwner(view.kwargs.get("institution"), user) or isStaff(view.kwargs.get("institution"), user):
                return True
        if "StaffTypeDetail" in str(view):
            staffInstitution = get_object_or_404(StaffType, pk=view.kwargs.get("pk")).custom_Type_For.id
            if isOwner(staffInstitution, user) or isStaff(staffInstitution, user):
                return True
        return False


class IsInstitutionPaid(BasePermission):
    message = "Changing privacy is not allowed if you don't have an existing subscription plan."

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        if request.data["privacy"]:

            if InstitutionSubscription.objects.filter(institution=view.kwargs.get("pk")):
                return True

        return False


class IsInstitutionVerified(BasePermission):
    message = "Action not allowed till this institution get verified."

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        if request.data["privacy"] != "public":
            return True
        if InstitutionVerification.verified.filter(institution=view.kwargs.get("pk")):
            return True

        return False


class IsNotInstitutionOwner(BasePermission):
    message = "You own this Institution"

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if get_object_or_404(Institution, pk=view.kwargs.get("institution")) == request.data["user"]:
            return True

        return False
