from rest_framework import generics, response, status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from classrooms.models import Classroom
from rest_framework.parsers import MultiPartParser, FormParser
from workspaces.models import Workspace
from .permissions import *
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
class SubmissionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (["status", "file__folder__workspace__id", "file__folder__workspace__classroom__id"],)
    queryset = Submission.objects.all()


class SubmissionDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = (["status", "file__folder__workspace__id", "file__folder__workspace__classroom__id"],)
    queryset = Recommendation.objects.all()


class RecommendationDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationSerializer
    queryset = Recommendation.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionResponseList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionResponseSerializer
    filter_backends = [SearchFilter]
    search_fields = (["submission", "responseStatus"],)
    queryset = SubmissionResponse.objects.all()


class SubmissionResponseDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionResponseSerializer
    queryset = SubmissionResponse.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationResponseList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationResponseSerializer
    filter_backends = [SearchFilter]
    search_fields = (["recommendation", "responseStatus"],)
    queryset = RecommendationResponse.objects.all()


class RecommendationResponseDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationResponseSerializer
    queryset = RecommendationResponse.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


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
