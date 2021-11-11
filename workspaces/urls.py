from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import *

app_name = "workspaces"

urlpatterns = [
    path("my-list", MyWorkspaceList.as_view(), name="my_workspace_list"),
    path("create", MyWorkspaceCreate.as_view(), name="my_workspace_list"),
    path("join", JoinWorkspaceView.as_view(), name="join_workspace"),
    path("shared", SharedWorkspaceListView.as_view(), name="shared_workspace"),
    path("members/<int:pk>", MemberListView.as_view(), name="member_List"),
    path("<int:pk>", MyWorkspaceRetrieve.as_view(), name="my_workspace_retrieve"),
    # folder
    path("folder-list/<int:pk>", WorkspaceFolderListView.as_view(), name="folder_list"),
    path("folder/<int:pk>", WorkspaceFolderModifyView.as_view(), name="folder_modify"),
    path("folder", WorkspaceFolderCreate.as_view(), name="folder_create"),
    # uploaded Files
    path("upload-file", WorkspaceUploadFileCreate.as_view(), name="workspace_upload_file"),
    path("upload-file/<int:pk>", WorkspaceUploadFileModify.as_view(), name="workspace_upload_modify"),
    path("upload-file-list/<int:pk>", WorkspaceUploadFileList.as_view(), name="workspace_upload_file_list"),
    # quill files
    path("quill-file", WorkspaceQuillFileCreate.as_view(), name="workspace_quill_file"),
    path("quill-file/<int:pk>", WorkspaceQuillFileModify.as_view(), name="workspace_quill_modify"),
    path("quill-file-list/<int:pk>", WorkspaceQuillFileList.as_view(), name="workspace_quill_file_list"),
]
