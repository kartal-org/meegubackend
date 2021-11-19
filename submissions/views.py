from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from classrooms.models import Classroom

# Create your views here.
class SubmissionList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSubmissionSerializer

    def get_queryset(self):
        return ClassroomSubmission.objects.filter(workspace__classroom=self.kwargs.get("classroom"))
