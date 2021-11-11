from django.urls import path

from .views import *

app_name = "notes"

urlpatterns = [
    path("<int:pk>", NotesRetrieve.as_view(), name="notes_retrieve"),
    path("", NotesListCreateView.as_view(), name="note_list_create"),
]
