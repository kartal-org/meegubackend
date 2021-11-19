from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *
from .permissions import *
from rest_framework.response import Response
from django.db.models import Avg


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class SearchArticleList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "title",
        "abstract",
        "author__first_name",
        "author__last_name",
        "publisher__name",
    ]
    queryset = Article.objects.filter(privacy="public")


class InstitutionArticleListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Article.objects.filter(publisher=self.kwargs["institution"])

    def perform_create(self, serializer):
        serializer.save(publisher=Institution.objects.get(pk=self.kwargs["institution"]))


class InstitutionArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]
    serializer_class = PostSerializer
    queryset = Article.objects.all()


class CommentListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(article=self.kwargs["article"])

    def perform_create(self, serializer):
        serializer.save(article=Article.objects.get(pk=self.kwargs["article"]), user=self.request.user)


class RatingList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        print(Rating.objects.filter(article=self.kwargs["article"]).aggregate(Avg("rate")))
        return Rating.objects.filter(article=self.kwargs["article"])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.aggregate(Avg("rate"))
        return Response({"rating": queryset.aggregate(Avg("rate"))["rate__avg"]})

    def perform_create(self, serializer):
        serializer.save(article=Article.objects.get(pk=self.kwargs["article"]), user=self.request.user)


class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer
    lookup_field = "article"

    def get_queryset(self):
        return Rating.objects.filter(article=self.kwargs["article"], user=self.request.user)
