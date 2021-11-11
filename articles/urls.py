from django.urls import path

from .views import *

app_name = "articles"

urlpatterns = [
    path("<int:pk>", ArticleRetrieve.as_view(), name="articles_retrieve"),
    path("", ArticleListView.as_view(), name="article_list"),
]
