from rest_framework.permissions import BasePermission, SAFE_METHODS
from institutions.models import Department


class IsStaff(BasePermission):
    message = "Managing Articles is for institution admin staff only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if obj.institution.owner == request.user:
            return True
        return False


class PublicationFileLimit(BasePermission):
    message = "Managing Articles is for institution admin staff only."

    def has_object(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        institutionLimit = Department.objects.get(id=request.data.get("department")).institution.storage_Limit
        institutionUsage = Department.objects.get(id=request.data.get("department")).institution.storage_used
        # Department.objects.get(id = 12).institution.storage_used
        size = int(request.data["size"])
        if institutionUsage + size >= institutionLimit:
            return False
        return True
