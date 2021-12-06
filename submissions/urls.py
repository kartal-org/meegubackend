from django.urls import path

from .views import *

urlpatterns = [
    path("", SubmissionList.as_view()),
    path("classroom", ClassroomSubmissionList.as_view()),
    path("change/<int:pk>", SubmissionDetail.as_view()),
    path("recommendation", RecommendationList.as_view()),
    path("recommendation/change/<int:pk>", RecommendationDetail.as_view()),
    path("recommendation/response", RecommendationResponseList.as_view()),
    path("recommendation/response/change/<int:pk>", RecommendationResponseDetail.as_view()),
    path("response", SubmissionResponseList.as_view()),
    path("response/change/<int:pk>", SubmissionResponseDetail.as_view()),
    # path("workspace/change/<int:pk>", WorkspaceSubmissionDetail.as_view(), name="workspace_submission_detail"),
    # path("classroom/<int:classroom>", ClassroomSubmissionList.as_view(), name="classroom_submission_list"),
    # path("classroom/change/<int:pk>", ClassroomSubmissionDetail.as_view(), name="classroom_submission_detail"),
    # path("institution/<int:institution>", InstitutionSubmissionList.as_view(), name="institution_submission_list"),
    # path("institution/change/<int:pk>", InstitutionSubmissionDetail.as_view(), name="institution_submission_detail"),
]
