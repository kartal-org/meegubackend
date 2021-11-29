from django.urls import path

from .views import *


urlpatterns = [
    # classroom
    path("classroom/<int:classroom>", ResourceListCreateView.as_view(), name="classroom_resource_list"),
    path("classroom/change/<int:pk>", ResourceDetailView.as_view(), name="classroom_resource_detail"),
    path("classroom/folder/change/<int:pk>", ResourceFolderDetail.as_view(), name="classroom_folder_detail"),
    path("classroom/folder/<int:resource>", ResourceFolderList.as_view(), name="classroom_folder_list"),
    path("classroom/file/change/<int:pk>", ClassroomResourceFileList.as_view(), name="classroom_file_detail"),
    path("classroom/file/<int:folder>", ClassroomResourceFileDetail.as_view(), name="classroom_file_list"),
    # Institution
    path("institution/<int:institution>", InstitutionResourceListCreateView.as_view(), name="classroom_resource_list"),
    path("institution/change/<int:pk>", InstitutionResourceDetailView.as_view(), name="classroom_resource_detail"),
]
