from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

from .permissions import *

# Create your views here.


class LibraryListCreateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LibraryItemSerializer

    def get_queryset(self):
        return LibraryItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LibraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LibraryItemSerializer

    def get_queryset(self):
        return LibraryItem.objects.filter(user=self.request.user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class AddLibraryList(generics.CreateAPIView):
#     """
#     This view will display all library items
#     """

#     permission_classes = [IsAuthenticated]
#     # queryset = Article.objects.all()
#     serializer_class = AddLibraryItemSerializer

#     def perform_create(self, serializer):
#         content = Article.objects.get(id=self.request.data["content"])

#         serializer.save(owner=self.request.user, content=content)
#         return Response([])


# class LibraryRetrieve(generics.RetrieveUpdateDestroyAPIView):
#     """
#     This view will retieve library items
#     """

#     permission_classes = [IsAuthenticated, IsOwner]
#     serializer_class = LibraryItemSerializer
#     queryset = LibraryItem.objects.all()
#     lookup_field = "pk"

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return Response(serializer.data, status=status.HTTP_200_OK)
