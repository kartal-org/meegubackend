from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *

# Create your views here.


class NotesListCreateView(generics.ListCreateAPIView):
    """
    This view will allow users to create and return list of notes
    """

    permission_classes = [IsAuthenticated]
    # queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner=user)


class NotesRetrieve(generics.RetrieveUpdateDestroyAPIView):
    """
    This view allows the student modify his notes
    """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    lookup_field = "pk"


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
