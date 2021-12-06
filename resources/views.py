from django.db.models import query
from rest_framework import generics, response, status, viewsets, filters

from institutions.models import Institution
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from classrooms.models import Classroom
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from workspaces.models import WorkspaceFile, WorkspaceFolder

from rest_framework.decorators import api_view, permission_classes


# CLassroom Resources
class ResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClasssroomResourceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "classroom__id",
    ]
    queryset = ClassroomResource.objects.all()


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClasssroomResourceSerializer
    queryset = ClassroomResource.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ResourceFolderList(generics.ListCreateAPIView):
    serializer_class = ClasssroomResourceFolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["resource__id"]
    queryset = ClassroomResourceFolder.objects.all()


class ResourceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClasssroomResourceFolderSerializer
    queryset = ClassroomResourceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomResourceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ClassroomResourceFileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["folder__id"]
    queryset = ClassroomResourceFile.objects.all()


class ClassroomResourceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomResourceFileSerializer
    queryset = ClassroomResourceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# Institution Resources


class InstitutionResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["institution__id"]
    queryset = InstitutionResource.objects.all()


class InstitutionDepartmentResourceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["department__id"]
    queryset = InstitutionResource.objects.all()


class InstitutionResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceSerializer
    queryset = InstitutionResource.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionResourceFolderList(generics.ListCreateAPIView):
    serializer_class = InstitutionResourceFolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["resource"]
    queryset = InstitutionResourceFolder.objects.all()


class InstitutionResourceFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceFolderSerializer
    queryset = InstitutionResourceFolder.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionResourceFileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceFileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["folder"]
    queryset = InstitutionResourceFolder.objects.all()


class InstitutionResourceFileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionResourceFileSerializer
    queryset = InstitutionResourceFile.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ImportResourceClass(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        files = ClassroomResourceFile.objects.filter(folder__resource=request.data.get("resource"))
        # breakpoint()

        for x in files:
            hello = WorkspaceFile.objects.create(
                folder=WorkspaceFolder.objects.get(id=request.data.get("folder")),
                # resource=request.data.get("to_resource"),
                name=x.name,
                tags=x.tags,
                file=x.file,
                content=x.content,
                size=x.size,
            )
            hello.save()
            print(hello.name)

        return response.Response(status=status.HTTP_200_OK)
