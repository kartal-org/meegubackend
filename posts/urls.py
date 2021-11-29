from django.urls import path

from .views import *

urlpatterns = [
    path("search", SearchArticleList.as_view(), name="article_search"),
    path("<int:institution>", InstitutionArticleListCreate.as_view(), name="institution_article_list"),
    path("archive", ArchiveListCreate.as_view(), name="archive_list"),
    path("change/<int:pk>", InstitutionArticleDetail.as_view(), name="institution_article_detail"),
    path("comment/<int:article>", CommentListCreate.as_view(), name="comment_list"),
    path("rating/<int:article>", RatingList.as_view(), name="rating_list"),
    path("rating/change/<int:article>", RatingDetail.as_view(), name="rating_detail"),
]
