from rest_framework import generics, response, status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.filters import SearchFilter

# Create your views here.


class NotesListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NotesSerializer
    filter_backends = [SearchFilter]
    search_fields = ["owner__id"]


class NotesRetrieve(generics.RetrieveUpdateDestroyAPIView):
    """
    This view allows the student modify his notes
    """

    permission_classes = [IsAuthenticated]
    serializer_class = NotesSerializer
    queryset = Note.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


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
