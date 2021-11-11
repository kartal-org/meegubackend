from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# from .permissions import *

# Create your views here.


class ArticleListView(generics.ListAPIView):
    """
    This view will display all articles
    """

    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleRetrieve(generics.RetrieveAPIView):
    """
    This view will retieve articles
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "pk"
