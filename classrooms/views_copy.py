from django.views import generic
from rest_framework import generics, response, status
from .models import *
from .serializers_copy import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import *
from rest_framework.views import APIView
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
import shortuuid
from django.db.models import Q


def get_classroom_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


# Adviser's Classroom Views
class AdviserClassroomListCreateView(generics.ListCreateAPIView):
    """Create and List view of Adviser's Classroom"""

    serializer_class = AdviserClassroomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        code = get_classroom_code()
        user = self.request.user
        serializer.save(code=code, owner=user)

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.filter(owner=user)


class AdviserClassroomModifyView(generics.RetrieveUpdateDestroyAPIView):
    """Allows Adviser to retrieve update and destroy his own classroom. Also use this as to retrieve student classroom"""

    serializer_class = AdviserClassroomSerializer
    permission_classes = [IsAuthenticated, IsClassroomAdviser, IsClassroomPaid]
    queryset = Classroom.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# Student's Classroom Views


class StudentClassroomJoinView(generics.CreateAPIView):
    """Let Student Join Classroom by entering the code"""

    permission_classes = [IsAuthenticated, IsClassroomPublic, IsNotClassroomOwner]
    serializer_class = JoinClassroomSerializer

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(user=user)


class StudentClassroomListView(generics.ListAPIView):
    """List Classroom of the Student"""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentClassroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(user=user)


class StudentTypeViewList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentTypeSerializer

    def get_queryset(self):
        classroom = self.kwargs["classroom"]
        return StudentType.objects.filter(Q(custom_Type_For__isnull=True) | Q(custom_Type_For=classroom))


class StudentTypeViewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsStudentTypeCreator]
    serializer_class = StudentTypeSerializer
    queryset = StudentType.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ClassroomStudentList(generics.ListAPIView):
    """This view display list of members the classroom have"""

    serializer_class = ClassroomStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        classroom = self.kwargs["classroom"]

        return Student.objects.filter(classroom=classroom)


class ClassroomStudentModify(generics.RetrieveUpdateDestroyAPIView):
    """This view will allow advisers to modify student membership in his classroom"""

    permission_classes = [IsAuthenticated]  # add is adviser permission
    serializer_class = ClassroomStudentSerializer
    queryset = Student.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
