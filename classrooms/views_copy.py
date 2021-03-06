from django.views import generic
from rest_framework import generics, response, status
from rest_framework import pagination
from .models import *
from .serializers_copy import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from .permissions_copy import *
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
import shortuuid
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from users.models import NewUser
from rest_framework.filters import SearchFilter, OrderingFilter


def get_classroom_code():
    codeID = shortuuid.ShortUUID().random(length=8)
    return codeID


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = "page_size"
#     max_page_size = 10


# Adviser's Classroom Views
class ClassroomCreateView(generics.CreateAPIView):

    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # institution = Institution.objects.get(id=self.request.data.get("institution")).id
        serializer.save(code=get_classroom_code())


class ClassroomListView(generics.ListAPIView):
    serializer_class = ClassroomListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["role"]

    def get_queryset(self):
        return ClassroomMember.objects.filter(user=self.request.user)


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsClassroomCreator]  # add is classroom adviser unya ha
    queryset = Classroom.objects.all()

    def update(self, request, *args, **kwargs):
        breakpoint()
        return super().update(request, *args, **kwargs)


class MemberCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberJoinSerializer


class MemberListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ["classroom__id"]
    queryset = ClassroomMember.objects.all()


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = ClassroomMember.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# class AdviserClassroomModifyView(generics.RetrieveUpdateDestroyAPIView):
#     """Allows Adviser to retrieve update and destroy his own classroom. Also use this as to retrieve student classroom"""

#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = AdviserClassroomSerializer
#     permission_classes = [IsAuthenticated, IsClassroomAdviser, IsInstitutionStaff]  # IsClassroomPaid
#     queryset = Classroom.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# # Student's Classroom Views


# class StudentClassroomJoinView(generics.CreateAPIView):
#     """Let Student Join Classroom by entering the code"""

#     permission_classes = [IsAuthenticated, IsClassroomPublic, IsNotClassroomOwner]
#     serializer_class = JoinClassroomSerializer

#     def perform_create(self, serializer):

#         user = self.request.user
#         serializer.save(user=user)


# class StudentClassroomListView(generics.ListAPIView):
#     """List Classroom of the Student"""

#     permission_classes = [IsAuthenticated]
#     serializer_class = StudentClassroomSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return ClassroomMember.objects.filter(user=user)


# # class StudentTypeViewList(generics.ListCreateAPIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = StudentTypeSerializer

# #     def get_queryset(self):
# #         classroom = self.kwargs["classroom"]
# #         return StudentType.objects.filter(Q(custom_Type_For__isnull=True) | Q(custom_Type_For=classroom))


# # class StudentTypeViewDetail(generics.RetrieveUpdateDestroyAPIView):
# #     permission_classes = [IsAuthenticated, IsStudentTypeCreator]
# #     serializer_class = StudentTypeSerializer
# #     queryset = StudentType.objects.all()

# #     def destroy(self, *args, **kwargs):
# #         serializer = self.get_serializer(self.get_object())
# #         super().destroy(*args, **kwargs)
# #         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class ClassroomStudentList(generics.ListCreateAPIView):
#     """This view display list of members the classroom have"""

#     serializer_class = ClassroomStudentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         classroom = self.kwargs["classroom"]

#         return ClassroomMember.objects.filter(classroom=classroom)

#     def perform_create(self, serializer):
#         serializer.save(
#             user=NewUser.objects.get(username=self.request.data.get("username")),
#             classroom=Classroom.objects.get(pk=self.kwargs["classroom"]),
#         )


# class ClassroomStudentModify(generics.RetrieveUpdateDestroyAPIView):
#     """This view will allow advisers to modify student membership in his classroom"""

#     permission_classes = [IsAuthenticated]  # add is adviser permission
#     serializer_class = ClassroomStudentSerializer
#     queryset = ClassroomMember.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class StudentList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ClassroomStudentSerializer

#     def get_queryset(self):
#         return ClassroomMember.objects.filter(classroom=self.kwargs.get("classroom"))
