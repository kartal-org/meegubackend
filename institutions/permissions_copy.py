from rest_framework.permissions import BasePermission, SAFE_METHODS
from subscriptions.models import *
from .models import Department, InstitutionVerification, Institution
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Staff, StaffType


class IsInstitutionCreator(BasePermission):
    message = "Managing Institution Detail is for creator only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsPermitStaffEdit(BasePermission):
    message = "Sorry you don't have a permission to edit staff."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.institution.creator == request.user
