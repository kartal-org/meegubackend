from django.urls import path

from .views import *

urlpatterns = [
    # classroom
    path("workspace/<int:workspace>", SubmissionList.as_view(), name="classroom_submission_list"),
]
