from rest_framework import generics, response, status, viewsets
from .models import *
from .serializers_copy import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from django.shortcuts import get_list_or_404, get_object_or_404
import shortuuid
from rest_framework.parsers import MultiPartParser, FormParser
from classrooms.models import ClassroomMember
from rest_framework.decorators import api_view
from itertools import chain
from django.db.models import F
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *

# Create your views here.
def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


class AdviserWorkspaceList(generics.ListAPIView):
    """List of workspace in a classroom"""

    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceListSerializer
    filter_backends = [SearchFilter]
    search_fields = ["classroom__id"]
    queryset = Workspace.objects.all()


class StudentWorkspaceList(generics.ListCreateAPIView):
    """List and Create view of workspace in a classroom relevant to a student"""

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceListSerializer
    # filter_fields = ("classroom__id", "members")
    # filter_class = WorkspaceFilter
    queryset = Workspace.objects.all()

    def get_queryset(self):
        member = ClassroomMember.objects.filter(user=self.request.user, classroom=self.kwargs.get("classroom"))
        return Workspace.objects.filter(members__in=member)

    def perform_create(self, serializer):
        serializer.save(classroom=Classroom.objects.get(id=self.kwargs.get("classroom")), code=get_code())


class WorkspaceDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceFolderList(generics.ListCreateAPIView):

    serializer_class = WorkspaceFolderSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkspaceFolder.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["workspace__id"]


class WorkspaceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFolderSerializer
    queryset = WorkspaceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFileSerializer
    queryset = WorkspaceFile.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["folder__id"]


class WorkspaceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFileSerializer
    queryset = WorkspaceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceMemberList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceMemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["id"]
    queryset = Workspace.objects.all()


class WorkspaceMemberCreate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceMemberSerializer
    queryset = Workspace.objects.all()


# class QuillFileList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = QuillSerializer

#     def get_queryset(self):
#         return WorkspaceFile.objects.filter(folder=self.kwargs["folder"])

#     def perform_create(self, serializer):
#         serializer.save(folder=WorkspaceFolder.objects.get(pk=self.kwargs["folder"]))


# class QuillFileDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = QuillSerializer
#     queryset = WorkspaceFile.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class UploadFileList(generics.ListCreateAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated, IsStudent, IsNotSubscriptionLimit]
#     serializer_class = UploadFileSerializer

#     def get_queryset(self):
#         return WorkspaceFile.objects.filter(folder=self.kwargs["folder"])

#     def perform_create(self, serializer):
#         serializer.save(folder=WorkspaceFolder.objects.get(pk=self.kwargs["folder"]))


# class UploadFileDetail(generics.RetrieveUpdateDestroyAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated, IsStudent]
#     serializer_class = UploadFileSerializer
#     queryset = WorkspaceFile.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# # @api_view()
# # def availableStudents(request, classroom):
# #     # rule for this is that students should only be able to join one workspace at one classroom
# #     if request.method == "GET":
# #         studentList = Student.objects.filter(classroom=classroom).values(
# #             uid=F("user__id"),
# #             first_name=F("user__first_name"),
# #             last_name=F("user__last_name"),
# #             username=F("user__username"),
# #         )
# #         memberList = Member.objects.filter(workspace__classroom__id=classroom).values(
# #             uid=F("user__id"),
# #             first_name=F("user__first_name"),
# #             last_name=F("user__last_name"),
# #             username=F("user__username"),
# #         )

# #         combineList = list(chain(studentList, memberList))

# #         available = list(map(dict, set(tuple(sorted(d.items())) for d in combineList)))

# #         res = [i for i in available if not (i["uid"] == 1)]
# #         res = [i for i in res if not (i["uid"] == request.user.id)]

# #         return response.Response(res)


# class MemberListCreate(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = WorkspacMemberSerializer

#     def get_queryset(self):
#         return Member.objects.filter(workspace=self.kwargs.get("workspace"))

#     def perform_create(self, serializer):
#         serializer.save(workspace=Workspace.objects.get(pk=self.kwargs["workspace"]))
