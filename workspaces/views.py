from django.views import generic
from rest_framework import generics, response, status, viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404, get_object_or_404
import shortuuid
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


class MyWorkspaceCreate(generics.CreateAPIView):
    """
    This view allows the student create his own workspace
    """

    permission_classes = [IsAuthenticated]
    queryset = Workspace.objects.all()
    serializer_class = CreateWorkspaceSerializer

    def perform_create(self, serializer):
        code = get_code()
        owner = self.request.user
        serializer.save(owner=owner, code=code)


class MyWorkspaceList(generics.ListAPIView):
    """
    This view allows the student see all of his own workspaces
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(owner=user)


class MyWorkspaceRetrieve(generics.RetrieveUpdateDestroyAPIView):
    """
    This view allows the student to retrieve, update and delete his workspace
    """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.all()
    lookup_field = "pk"


class JoinWorkspaceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JoinWorkspaceSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(user=user)
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data["workspace"]
        ques = get_object_or_404(Workspace, code=code)

        if user == ques.owner:
            print("captured")
            return response.Response(
                {"error": "You own this workspace"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        code = serializer.data["workspace"]
        qs = get_object_or_404(Workspace, code=code)
        print(qs)
        serializer.data["workspaceId"] = qs.id
        newPayload = {
            "workspaceID": qs.id,
            "name": qs.name,
            "status": qs.status,
            "description": qs.description,
            "code": serializer.data["workspace"],
            "id": serializer.data["id"],
        }

        return response.Response(newPayload, status=status.HTTP_201_CREATED, headers=headers)


class MemberListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceMemberSerializers

    def get_queryset(self):
        workspace = self.kwargs["pk"]
        return Member.objects.filter(workspace=workspace)


class SharedWorkspaceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SharedWorkspaceSerializer

    def get_queryset(self):
        user = self.request.user
        return Member.objects.filter(user=user)


class WorkspaceFolderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFolderSerializer

    def get_queryset(self):
        workspace = self.kwargs["pk"]
        return WorkspaceFolder.objects.filter(workspace=workspace)


class WorkspaceFolderCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFolderSerializer


class WorkspaceFolderModifyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceFolderSerializer
    lookup_field = "pk"
    queryset = WorkspaceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceUploadFileCreate(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceUploadFileSerializer
    queryset = WorkspaceUploadedFile.objects.all()


class WorkspaceUploadFileList(generics.ListAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceUploadFileSerializer

    def get_queryset(self):
        folder = self.kwargs.get("pk")
        return WorkspaceUploadedFile.objects.filter(folder=folder)


class WorkspaceUploadFileModify(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceUploadFileSerializer
    queryset = WorkspaceUploadedFile.objects.all()
    lookup_field = "pk"

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceQuillFileCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceQuillFileSerializer
    queryset = WorkspaceQuillFile.objects.all()


class WorkspaceQuillFileList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceQuillFileSerializer

    def get_queryset(self):
        folder = self.kwargs.get("pk")
        return WorkspaceQuillFile.objects.filter(folder=folder)


class WorkspaceQuillFileModify(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceQuillFileSerializer
    queryset = WorkspaceQuillFile.objects.all()
    lookup_field = "pk"

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
