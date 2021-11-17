from django.urls import path
from ..views.classroom_views import *

urlpatterns = [
    # classroom
    path("<int:pk>", ResourceListCreateView.as_view(), name="classroom_resource_list"),
    path("detail/<int:pk>", ResourceDetailView.as_view(), name="classroom_resource_detail"),
    path("folder-detail/<int:pk>", ResourceFolderDetail.as_view(), name="classroom_folder_detail"),
    path("folder-list/<int:resource>", ResourceFolderList.as_view(), name="classroom_folder_list"),
    path("file-detail/<int:pk>", ResourceQuillFileDetail.as_view(), name="classroom_file_detail"),
    path("file-list/<int:folder>", ResourceQuillFileList.as_view(), name="classroom_file_list"),
    path("uploadfile-detail/<int:pk>", ResourceUploadFileDetail.as_view(), name="classroom_uploadfile_detail"),
    path("uploadfile-list/<int:folder>", ResourceUploadFileList.as_view(), name="classroom_uploadfile_list"),
]
