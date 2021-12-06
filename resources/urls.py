from django.urls import path

from .views import *


urlpatterns = [
    # classroom
    path("classroom", ResourceListCreateView.as_view()),
    path("classroom/change/<int:pk>", ResourceDetailView.as_view()),
    path("classroom/folder", ResourceFolderList.as_view()),
    path("classroom/folder/change/<int:pk>", ResourceFolderDetail.as_view()),
    path("classroom/file", ClassroomResourceFileList.as_view()),
    path("classroom/file/change/<int:pk>", ClassroomResourceFileDetail.as_view()),
    # Institution
    path("institution", InstitutionResourceListCreateView.as_view()),
    path("institution/change/<int:pk>", InstitutionResourceDetailView.as_view()),
    path("institution/folder", InstitutionResourceFolderList.as_view()),
    path("institution/folder/change/<int:pk>", InstitutionResourceFolderDetail.as_view()),
    path("institution/file", InstitutionResourceFileList.as_view()),
    path("institution/file/change/<int:pk>", InstitutionResourceFileDetail.as_view()),
    # Department
    path("institution/department", InstitutionDepartmentResourceListCreateView.as_view()),
    path("import-classroom", ImportResourceClass.as_view(), name="import_classroom_resource"),
]
