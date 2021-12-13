from django.db import connection
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework import response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from institutions.models import Department
from .serializers_copy import *
from .models import *
from .permissions import *
from rest_framework.response import Response
from django.db.models import Avg, OuterRef, Subquery
from workspaces.models import Workspace
from rest_framework.decorators import api_view, parser_classes, permission_classes
from django.db.models import F
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
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


class ArticleSearch(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, PublicationFileLimit]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PublicationSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title"]
    ratings = Rating.objects.filter(publication=OuterRef("pk"))
    queryset = Publication.objects.annotate(rating_you=Subquery(ratings.values("rate"))).order_by("-rating_you")


class ArticleListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, PublicationFileLimit]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PublicationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["^title", "department__id", "department__institution__name", "category__name"]
    # ratings = Rating.objects.filter(publication=OuterRef("pk"))
    # queryset = Publication.objects.annotate(rating_you=Subquery(ratings.values("rate"))).order_by("-rating_you")
    queryset = Publication.objects.all()

    # .annotate(num_authors=Count('authors')).order_by('num_authors')

    def perform_create(self, serializer):
        if self.request.data.get("submission"):
            serializer.save(submission=Submission.objects.get(pk=self.request.data.get("submission")))
        serializer.save()


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RatingListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # search_fields = ["publication__id", "user__id"]
    filterset_fields = ("publication__id", "user__id")
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CommentListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["publication__id"]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


# class InstitutionArticleListCreate(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def get_queryset(self):
#         return Publication.objects.filter(department__institution=self.kwargs["institution"])

#     def perform_create(self, serializer):
#         serializer.save(
#             department=Department.objects.get(pk=self.request.data.get("department")),
#             # workspace=Workspace.objects.get(pk=self.request.data.get("workspace")),
#         )

#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         print("Queries count is: {}".format(len(connection.queries)))
#         return response


# class ArchiveListCreate(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ArchiveSerializer
#     queryset = Publication.objects.all()


# class InstitutionArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsStaff]
#     serializer_class = ArticleDetailSerializer
#     queryset = Publication.objects.all()


# class CommentListCreate(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         return Comment.objects.filter(article=self.kwargs["article"])

#     def perform_create(self, serializer):
#         serializer.save(article=Publication.objects.get(pk=self.kwargs["article"]), user=self.request.user)


# class RatingList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RatingSerializer

#     def get_queryset(self):
#         print(Rating.objects.filter(article=self.kwargs["article"]).aggregate(Avg("rate")))
#         return Rating.objects.filter(article=self.kwargs["article"])

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         queryset.aggregate(Avg("rate"))
#         return Response({"rating": queryset.aggregate(Avg("rate"))["rate__avg"]})

#     def perform_create(self, serializer):
#         serializer.save(article=Publication.objects.get(pk=self.kwargs["article"]), user=self.request.user)


# class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RatingSerializer
#     lookup_field = "article"

#     def get_queryset(self):
#         return Rating.objects.filter(article=self.kwargs["article"], user=self.request.user)


# @api_view()
# def articleView(request):
#     """Create and Get Articles"""
#     if request.method == "GET":
#         # what do we want? All article fields, Authors, and Institution
#         workspaceList = list(Publication.objects.values_list("file", flat=True))
#         authorList = [member.user.full_name for member in Member.objects.filter(workspace__id__in=workspaceList)]
#         article = Publication.objects.all()
#         Publication.objects.all().values(workspace=F("file__folder__workspace"))
#         #  membersList
#         # [member.user.full_name for member in Member.objects.filter(workspace__id__in=workspaceList)]
#         # return Response(article)
#         # Every Article has workspacefile
#     pass
