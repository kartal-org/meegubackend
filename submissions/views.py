# from rest_framework import generics, response, status
# from .serializers import *
# from .models import *
# from rest_framework.permissions import IsAuthenticated
# from classrooms.models import Classroom
# from rest_framework.parsers import MultiPartParser, FormParser
# from workspaces.models import Workspace
# from .permissions import *
# from rest_framework.filters import SearchFilter, OrderingFilter

# # Create your views here.
# class SubmissionList(generics.ListCreateAPIView):
#     # parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubmissionDetailSerializer

#     def get_queryset(self):
#         return Submission.objects.filter(file__folder__workspace=self.kwargs.get("workspace"))

#     # def perform_create(self, serializer):
#     #     serializer.save(workspace=Workspace.objects.get(pk=self.kwargs.get("workspace")))


# class WorkspaceSubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsMember]
#     serializer_class = SubmissionDetailSerializer
#     queryset = Submission.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class ClassroomSubmissionList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubmissionDetailSerializer

#     def get_queryset(self):
#         return Submission.objects.filter(workspace__classroom=self.kwargs.get("classroom"))


# class ClassroomSubmissionDetail(generics.RetrieveUpdateAPIView):
#     permission_classes = [IsAuthenticated, IsAdviser]
#     serializer_class = SubmissionDetailSerializer
#     queryset = Submission.objects.all()


# class InstitutionSubmissionList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SubmissionDetailSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = [
#         "institutionResponse",
#     ]

#     def get_queryset(self):
#         return Submission.objects.filter(institution=self.kwargs.get("institution"))


# class InstitutionSubmissionDetail(generics.RetrieveUpdateAPIView):
#     permission_classes = [IsAuthenticated, IsAdviser]
#     serializer_class = SubmissionDetailSerializer
#     queryset = Submission.objects.filter(institution__isnull=False)
