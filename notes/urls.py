from django.urls import path

from .views import *

app_name = "notes"

urlpatterns = [
    path("", NotesListCreateView.as_view()),
    path("change/<int:pk>", NotesRetrieve.as_view()),
]
