from django.urls import path


from .views_copy import *

app_name = "workspaces"

urlpatterns = [
    path("<int:classroom>", WorkspaceList.as_view(), name="workspace_list"),
    path("change/<int:pk>", WorkspaceDetail.as_view(), name="workspace_detail"),
    path("folder/<int:workspace>", WorkspaceFolderList.as_view(), name="folder_list"),
    path("folder/change/<int:pk>", WorkspaceFolderDetail.as_view(), name="folder_detail"),
    path("file/<int:folder>", QuillFileList.as_view(), name="file_list"),
    path("file/change/<int:pk>", QuillFileDetail.as_view(), name="file_detail"),
    path("upload-file/<int:folder>", UploadFileList.as_view(), name="upload_file_list"),
    path("upload-file/change/<int:pk>", UploadFileDetail.as_view(), name="upload_file_detail"),
    path("user/<int:classroom>", SharedWorkspaceList.as_view(), name="user_workspace_list"),
]
