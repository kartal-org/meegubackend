from django.urls import path

from .views import *

urlpatterns = [
    path("", ArticleListCreate.as_view()),
    path("search", ArticleSearch.as_view()),
    path("change/<int:pk>", ArticleDetailView.as_view()),
    path("rating", RatingListCreate.as_view()),
    path("rating/change/<int:pk>", RatingDetail.as_view()),
    path("comment", CommentListCreate.as_view()),
    path("comment/change/<int:pk>", CommentDetail.as_view()),
    path("category", CategoryList.as_view()),
]
