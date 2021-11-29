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


# Create your views here.
def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


class WorkspaceList(generics.ListCreateAPIView):
    """List Create View of all workspace in the classroom (Adviser)"""

    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.filter(classroom=self.kwargs["classroom"])

    def perform_create(self, serializer):
        serializer.save(
            classroom=Classroom.objects.get(pk=self.kwargs["classroom"]), code=get_code(), creator=self.request.user
        )


class WorkspaceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceFolderList(generics.ListCreateAPIView):
    """List Create Workpace Folder"""

    # This allows students create folders
    # Adviser can only see this folders
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return WorkspaceFolder.objects.filter(workspace=self.kwargs["workspace"])

    def perform_create(self, serializer):
        serializer.save(workspace=Workspace.objects.get(pk=self.kwargs["workspace"]))


class WorkspaceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = FolderSerializer
    queryset = WorkspaceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def get_queryset(self):
        return WorkspaceFile.objects.filter(folder=self.kwargs["folder"])

    def perform_create(self, serializer):
        serializer.save(folder=WorkspaceFolder.objects.get(pk=self.kwargs["folder"]))


class WorkspaceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer
    queryset = WorkspaceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class QuillFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuillSerializer

    def get_queryset(self):
        return WorkspaceQuillFile.objects.filter(folder=self.kwargs["folder"])

    def perform_create(self, serializer):
        serializer.save(folder=WorkspaceFolder.objects.get(pk=self.kwargs["folder"]))


class QuillFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuillSerializer
    queryset = WorkspaceQuillFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class UploadFileList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsStudent, IsNotSubscriptionLimit]
    serializer_class = UploadFileSerializer

    def get_queryset(self):
        return WorkspaceUploadedFile.objects.filter(folder=self.kwargs["folder"])

    def perform_create(self, serializer):
        serializer.save(folder=WorkspaceFolder.objects.get(pk=self.kwargs["folder"]))


class UploadFileDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = UploadFileSerializer
    queryset = WorkspaceUploadedFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# Untested


# class SharedWorkspaceList(generics.ListCreateAPIView):
#     """List of all student's workspace in a classroom and able them to join by workspace code"""

#     permission_classes = [IsAuthenticated, IsNotAMember]
#     serializer_class = SharedWorkspaceSerializer

#     def get_queryset(self):
#         return Member.objects.filter(classroom=self.kwargs["classroom"], user=self.request.user)

#     def perform_create(self, serializer):

#         serializer.save(
#             user=self.request.user, workspace=get_object_or_404(Workspace, code=self.request.data["workspace"]).id
#         )
#         return super().perform_create(serializer)


# class AvailableStudentList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = WorkspacMemberSerializer

#     def get_queryset(self):
#         breakpoint()
#         studentList = Student.objects.filter(classroom=self.kwargs.get("classroom")).values_list(
#             "user__id", "user__first_name", "user__last_name", "user__username"
#         )
#         memberList = Member.objects.filter(workspace__classroom__id=self.kwargs.get("classroom")).values_list(
#             "user__id", "user__first_name", "user__last_name", "user__username"
#         )
#         available = list(set(studentList) ^ set(memberList))
#         return available

#     pass


@api_view()
def availableStudents(request, classroom):
    # rule for this is that students should only be able to join one workspace at one classroom
    if request.method == "GET":
        studentList = Student.objects.filter(classroom=classroom).values(
            uid=F("user__id"),
            first_name=F("user__first_name"),
            last_name=F("user__last_name"),
            username=F("user__username"),
        )
        memberList = Member.objects.filter(workspace__classroom__id=classroom).values(
            uid=F("user__id"),
            first_name=F("user__first_name"),
            last_name=F("user__last_name"),
            username=F("user__username"),
        )

        combineList = list(chain(studentList, memberList))

        available = list(map(dict, set(tuple(sorted(d.items())) for d in combineList)))

        res = [i for i in available if not (i["uid"] == 1)]
        res = [i for i in res if not (i["uid"] == request.user.id)]

        return response.Response(res)


class MemberListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspacMemberSerializer

    def get_queryset(self):
        return Member.objects.filter(workspace=self.kwargs.get("workspace"))

    def perform_create(self, serializer):
        serializer.save(workspace=Workspace.objects.get(pk=self.kwargs["workspace"]))
