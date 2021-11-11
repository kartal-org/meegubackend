from django.urls import path

from .views import *

app_name = "libraries"

urlpatterns = [
    path("<int:pk>", LibraryRetrieve.as_view(), name="libraryItems_retrieve"),
    path("", LibraryListCreateView.as_view(), name="libraryItem_list"),
    path("add", AddLibraryList.as_view(), name="libraryItem_listadd"),
]
