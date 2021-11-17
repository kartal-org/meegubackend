from rest_framework import generics
from ..models.classroom_models import *
from ..permissions import *
from ..serializers.classroom_serializer import *
from rest_framework.permissions import IsAuthenticated


class ResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClasssroomResourceSerializer

    def get_queryset(self):
        return ClassroomResource.objects.filter(classroom=self.kwargs["pk"])

    def perform_create(self, serializer):
        serializer.save(classroom=Classroom.objects.get(pk=self.kwargs["pk"]))


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClasssroomResourceSerializer
    queryset = ClassroomResource.objects.all()


class ResourceFolderList(generics.ListCreateAPIView):
    serializer_class = ClasssroomResourceFolderSerializer
    permission_classes = [IsAuthenticated, IsClassroomAdviser]

    def get_queryset(self):
        return ClassroomResourceFolder.objects.filter(resource=self.kwargs["resource"])

    def perform_create(self, serializer):
        serializer.save(resource=ClassroomResource.objects.get(pk=self.kwargs["resource"]))


class ResourceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClasssroomResourceFolderSerializer
    queryset = ClassroomResourceFolder.objects.all()


class ResourceQuillFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClassroomResourceQuillFileSerializer

    def get_queryset(self):
        return ClassroomResourceQuillFile.objects.filter(
            folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"]))


class ResourceQuillFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClassroomResourceQuillFileSerializer
    queryset = ClassroomResourceQuillFile.objects.all()


class ResourceUploadFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser, IsNotSubscriptionLimit]
    serializer_class = ClassroomResourceUploadedFileSerializer

    def get_queryset(self):
        return ClassroomResourceUploadedFile.objects.filter(
            folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"]))


class ResourceUploadFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClassroomResourceUploadedFileSerializer
    queryset = ClassroomResourceUploadedFile.objects.all()
