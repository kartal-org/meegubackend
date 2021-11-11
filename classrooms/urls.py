from django.urls import path

from .views import *

app_name = "classrooms"

urlpatterns = [
    # For Adviser
    path("<int:pk>/", ClassroomEdit.as_view(), name="detailcreate"),
    path("create", ClassroomCreate.as_view(), name="classroom_listcreate"),
    path("list", ClassroomListAdviser.as_view(), name="classroom_listcreate"),
    # path("members/", AdviserApplicationClassroom.as_view(), name="classroom_members"),
    # For students
    path("myclass", ClassroomList.as_view(), name="myclassroom_list"),
    path("find/<str:code>", ReturnClassroomByCodeView.as_view(), name="find_classroom_by_code"),
    path("join/", NewClassroomJoinView.as_view(), name="joinclassroom"),
    path("members/<int:pk>", ClassroomMemberList.as_view(), name="classroom_member_list"),
    path("members/modify/<int:pk>", ClassroomMemberModify.as_view(), name="classroom_member_list_modify"),
    # For Resources
    path("resources-modify/<int:pk>/", ResourceModifyView.as_view(), name="resources_modify"),
    path("resources-list/<int:pk>/", ResourceListAPIView.as_view(), name="resources_list"),
    path("resources-create/", ResourceCreateAPIView.as_view(), name="resources_create"),
    path("resources-folder/<int:pk>", ResourceFolderModify.as_view(), name="resources-folder_edit"),
    path("resources-folder-list/<int:pk>", ResourceFolderList.as_view(), name="resources-folder_list"),
    path("resources-folder/", ResourceFolderCreate.as_view(), name="resources-folder_create"),
    path("resources-file/upload", FileUploadedListCreate.as_view(), name="resources-uploadFile_Listcreate"),
    path("resources-file/upload-list", FileUploadList.as_view(), name="resources-uploadFile_Listcreate"),
    path("resources-file/<int:pk>", FileQuillModify.as_view(), name="resources-quillFile_Modify"),
    path("resources-file/", FileQuillListCreate.as_view(), name="resources-quillFile_Listcreate"),
    path("resources-file/upload/<int:pk>", FileUploadedModify.as_view(), name="resources-uploadFile_Modify"),
    # # path("folders/", Folders.as_view(), name="listfolders"),
    # # # path("files/", Files.as_view(), name="listfiles"),
    # # path("files/", Files.as_view(), name="listfiles"),
]
