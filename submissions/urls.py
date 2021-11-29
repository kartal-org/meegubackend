from django.urls import path

from .views import *

urlpatterns = [
    path("workspace/<int:workspace>", SubmissionList.as_view(), name="workspace_submission_list"),
    path("workspace/change/<int:pk>", WorkspaceSubmissionDetail.as_view(), name="workspace_submission_detail"),
    path("classroom/<int:classroom>", ClassroomSubmissionList.as_view(), name="classroom_submission_list"),
    path("classroom/change/<int:pk>", ClassroomSubmissionDetail.as_view(), name="classroom_submission_detail"),
    path("institution/<int:institution>", InstitutionSubmissionList.as_view(), name="institution_submission_list"),
    path("institution/change/<int:pk>", InstitutionSubmissionDetail.as_view(), name="institution_submission_detail"),
]
