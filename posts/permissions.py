from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaff(BasePermission):
    message = "Managing Articles is for institution admin staff only."

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        if obj.institution.owner == request.user:
            return True
        return False
