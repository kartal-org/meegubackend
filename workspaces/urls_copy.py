from django.urls import path


from .views_copy import *

app_name = "workspaces"

urlpatterns = [
    path("", WorkspaceList.as_view()),
    path("student/<int:classroom>", StudentWorkspaceList.as_view()),
    path("join/", JoinWorkspaceView.as_view()),
    path("change/<int:pk>", WorkspaceDetail.as_view()),
    path("folder", WorkspaceFolderList.as_view()),
    path("folder/<int:pk>", WorkspaceFolderDetail.as_view()),
    path("file", WorkspaceFileList.as_view()),
    path("file/<int:pk>", WorkspaceFileDetail.as_view()),
    path("member", WorkspaceMemberList.as_view()),
    path("member/create", WorkspaceMemberCreate.as_view()),
    path("member/<int:pk>", WorkspaceMemberDetail.as_view()),
    # path("member/change/<int:pk>", WorkspaceMemberDetail.as_view()),
    # path("change/<int:pk>", WorkspaceDetail.as_view(), name="workspace_detail"),
    # path("folder/<int:workspace>", WorkspaceFolderList.as_view(), name="folder_list"),
    # path("folder/change/<int:pk>", WorkspaceFolderDetail.as_view(), name="folder_detail"),
    # path("file/<int:folder>", WorkspaceFileList.as_view(), name="file_list"),
    # path("file/change/<int:pk>", WorkspaceFileDetail.as_view(), name="file_detail"),
    # path("upload-file/<int:folder>", UploadFileList.as_view(), name="upload_file_list"),
    # path("upload-file/change/<int:pk>", UploadFileDetail.as_view(), name="upload_file_detail"),
    # # path("user/<int:classroom>", SharedWorkspaceList.as_view(), name="user_workspace_list"),
    # path("members/<int:workspace>", MemberListCreate.as_view(), name="member_list"),
    # # path("members/available/<int:classroom>", availableStudents, name="available_member_list"),
]
