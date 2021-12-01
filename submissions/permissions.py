# from rest_framework.permissions import BasePermission, SAFE_METHODS
# from workspaces.models import Member
# from django.core.exceptions import ObjectDoesNotExist


# class IsAdviser(BasePermission):
#     message = "Only Adviser of Classroom can edit submission adviser response"

#     def has_object_permission(self, request, view, obj):

#         if request.method in SAFE_METHODS:
#             return True
#         return obj.workspace.classroom.owner == request.user


# class IsMember(BasePermission):
#     message = "Only Member can edit submission "

#     def has_object_permission(self, request, view, obj):

#         if request.method in SAFE_METHODS:
#             return True
#         workspaceID = obj.workspace.id
#         try:
#             Member.objects.get(workspace=workspaceID, user=request.user)
#             return True
#         except ObjectDoesNotExist:
#             return False
