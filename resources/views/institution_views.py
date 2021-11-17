from rest_framework import generics
from ..models.institution_models import *
from ..permissions import *
from ..serializers.institution_serializer import *
from institutions.models import Institution
from rest_framework.permissions import IsAuthenticated


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


class InstitutionResourceQuillFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceQuillFileSerializer

    def get_queryset(self):
        return InstitutionResourceQuillFile.objects.filter(
            folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"]))


class InstitutionResourceQuillFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceQuillFileSerializer
    queryset = InstitutionResourceQuillFile.objects.all()


class InstitutionResourceUploadFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff, IsNotSubscriptionLimit]
    serializer_class = InstitutionResourceUploadedFileSerializer

    def get_queryset(self):
        return InstitutionResourceUploadedFile.objects.filter(
            folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"])
        )

    def perform_create(self, serializer):
        serializer.save(folder=InstitutionResourceFolder.objects.get(pk=self.kwargs["folder"]))


class InstitutionResourceUploadFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionStaff]
    serializer_class = InstitutionResourceUploadedFileSerializer
    queryset = InstitutionResourceUploadedFile.objects.all()
