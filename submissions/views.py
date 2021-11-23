from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from classrooms.models import Classroom
from rest_framework.parsers import MultiPartParser, FormParser
from workspaces.models import Workspace

# Create your views here.
class SubmissionList(generics.ListCreateAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSubmissionSerializer

    def get_queryset(self):
        return ClassroomSubmission.objects.filter(workspace=self.kwargs.get("workspace"))

    def perform_create(self, serializer):
        serializer.save(workspace=Workspace.objects.get(pk=self.kwargs.get("workspace")))
