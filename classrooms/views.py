from django.views import generic
from rest_framework import generics, response, status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404
from rest_framework.parsers import MultiPartParser, FormParser
import shortuuid


class ClassroomListAdviser(generics.ListAPIView):
    """This view will let Adviser see his classrooms"""

    # print(IsAuthenticated)
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Classroom.objects.all()
    serializer_class = ListClassroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.filter(owner=user)


def get_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


class ClassroomCreate(generics.CreateAPIView):
    """This view will let Adviser create his classrooms"""

    # print(IsAuthenticated)
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Classroom.objects.all()
    serializer_class = CreateClassroomSerializer

    def perform_create(self, serializer):
        code = get_code()
        serializer.save(code=code)


class NewClassroomJoinView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JoinClassroomSerializer


class ClassroomList(generics.ListAPIView):
    """This view will let student retrieve classrooms that his in. Note: need the NewUser.id in the request even though this is get"""

    permission_classes = [permissions.IsAuthenticated]  # IsAMemberPermission
    # queryset = Student.objects.all()
    serializer_class = GetStudentsClassroomsSerializer

    def get_queryset(self):  # this will filter resources according to classroom
        student = self.request.user
        return Student.objects.filter(student=student)

    # lookup_field = "student"


class ClassroomMemberList(generics.ListAPIView):
    """This view display list of members the classroom have"""

    serializer_class = MemberSerializers
    # queryset = Student.objects.all()

    def get_queryset(self):  # this will filter resources according to classroom
        classroom = self.kwargs["pk"]
        return Student.objects.filter(classroom=classroom)


# What if I want to remove or something a student from classroom
class ClassroomMemberModify(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow advisers to modify student membership in his classroom"""

    serializer_class = ClassroomMembersSerializerModify
    queryset = Student.objects.all()
    lookup_field = "pk"


class ClassroomEdit(generics.RetrieveUpdateDestroyAPIView):
    """
    This view allows the owner of the classroom to modify it.
    """

    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "pk"
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


# a student will join in a classroom by code

# Step 1: Find Classroom by id
class ReturnClassroomByCodeView(generics.ListAPIView):
    serializer_class = ReturnClassroomByCode

    def get_queryset(self):  # this will filter resources according to classroom
        code = self.kwargs["code"]
        return Classroom.objects.filter(code=code)


# Step to join the classroom
class ClassroomMembers(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = JoinClassroomSerializers


class ResourceCreateAPIView(generics.CreateAPIView):
    """This view will allow Adviser to create and see list of resources he created in his classroom"""

    permission_classes = [permissions.IsAuthenticated]  # also add CustomIsowner
    serializer_class = ResourcesSerializer
    # queryset = ClassroomResource.objects.all()


class ResourceListAPIView(generics.ListAPIView):
    """This view will allow Adviser to create and see list of resources he created in his classroom"""

    permission_classes = [permissions.IsAuthenticated]  # also add CustomIsowner
    serializer_class = ResourcesSerializer

    def get_queryset(self):  # this will filter resources according to classroom
        classroom = self.kwargs["pk"]
        return ClassroomResource.objects.filter(classroom=classroom)


class ResourceModifyView(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow Adviser to modify resource he created in his classroom"""

    # permission_classes = [permissions.IsAuthenticated] #add custom Permission Later
    queryset = ClassroomResource.objects.all()
    serializer_class = ResourcesSerializer
    lookup_field = "pk"


class ResourceFolderCreate(generics.ListCreateAPIView):
    """This view will allow Adviser to create and see list of folder he created in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourcesFolderSerializer

    def get_queryset(self):
        user = self.request.user
        return ClassroomResourceFolder.objects.filter(resource__classroom__owner=user)


class ResourceFolderList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourcesFolderSerializer

    def get_queryset(self):
        resource = self.kwargs["pk"]
        return ClassroomResourceFolder.objects.filter(resource=resource)


class ResourceFolderModify(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow Adviser to modify of folder he created in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourcesFolderSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return ClassroomResourceFolder.objects.filter(resource__classroom__owner=user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class FileUploadedListCreate(APIView):
    """This view will allow Adviser to create and see list of files he uploaded in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileQuillListCreate(generics.ListCreateAPIView):
    """This view will allow Adviser to create and see list of files he created in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    queryset = ClassroomResourceQuillFile.objects.all()
    serializer_class = FileQuillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=folder__id"]

    # def get_queryset(self):
    #     user = self.request.user
    #     return QuillFile.objects.filter(folder__resource__classroom__owner=user)


class FileUploadList(generics.ListAPIView):
    """This view will allow Adviser to create and see list of files he created in his resources"""

    permission_classes = [permissions.IsAuthenticated]

    queryset = ClassroomResourceUploadedFile.objects.all()
    serializer_class = FileUploadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=folder__id"]

    # def get_queryset(self):
    #     user = self.request.user
    #     return ClassroomResourceUploadedFile.objects.filter(folder__resource__classroom__owner=user)


class FileUploadedModify(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow Adviser to create and see list of files he uploaded in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return ClassroomResourceUploadedFile.objects.filter(folder__resource__classroom__owner=user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class FileQuillModify(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow Adviser to create and see list of files he created in his resources"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileQuillSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return ClassroomResourceQuillFile.objects.filter(folder__resource__classroom__owner=user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class GetQuillFilesBasedOnFolder(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileQuillSerializer

    def get_queryset(self):
        folder = self.kwargs["pk"]
        return ClassroomResourceQuillFile.objects.filter(folder=folder)


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
