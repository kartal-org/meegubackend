from django.urls import path

from .views import *

urlpatterns = [
    # classroom
    path("classroom/<int:classroom>", SubmissionList.as_view(), name="classroom_submission_list"),
]
