from django.urls import path

from .views import *

app_name = "libraries"

urlpatterns = [
    path("", LibraryListCreateView.as_view()),
    path("change/<int:pk>", LibraryDetailView.as_view()),
]
