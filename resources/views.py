from django.db.models import query
from rest_framework import generics, response, status, viewsets, filters

from institutions.models import Institution
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from classrooms.models import Classroom


# CLassroom Resources
class ResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClasssroomResourceSerializer

    def get_queryset(self):
        return ClassroomResource.objects.filter(classroom=self.kwargs["classroom"])

    def perform_create(self, serializer):
        serializer.save(classroom=Classroom.objects.get(pk=self.kwargs["classroom"]))


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClasssroomResourceSerializer
    queryset = ClassroomResource.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


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

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomResourceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClassroomResourceFileSerializer

    def get_queryset(self):
        return ClassroomResourceFile.objects.filter(
            folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=ClassroomResourceFolder.objects.get(pk=self.kwargs["folder"]))


class ClassroomResourceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsClassroomAdviser]
    serializer_class = ClassroomResourceFileSerializer
    queryset = ClassroomResourceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# Institution Resources


class InstitutionResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceSerializer

    def get_queryset(self):
        return InstitutionResource.objects.filter(institution=self.kwargs["institution"])

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


class InstitutionResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceSerializer
    queryset = InstitutionResource.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionResourceFolderList(generics.ListCreateAPIView):
    serializer_class = InstitutionResourceFolderSerializer
    permission_classes = [IsAuthenticated, IsInstitutionStaff]

    def get_queryset(self):
        return InstitutionResourceFolder.objects.filter(resource=self.kwargs["resource"])

    def perform_create(self, serializer):
        serializer.save(resource=InstitutionResource.objects.get(pk=self.kwargs["resource"]))


class InstitutionResourceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceFolderSerializer
    queryset = InstitutionResourceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionResourceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceFileSerializer

    def get_queryset(self):
        return InstitutionResourceFile.objects.filter(
            folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"]))


class InstitutionResourceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceFileSerializer
    queryset = InstitutionResourceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
