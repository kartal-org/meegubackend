from django.urls import path

from .views_copy import *

app_name = "classrooms"

urlpatterns = [
    # For Adviser
    path("<int:pk>", AdviserClassroomModifyView.as_view(), name="adviserClassroom_modify"),
    path("", AdviserClassroomListCreateView.as_view(), name="adviserClassroom"),
    # For Students
    path("join", StudentClassroomJoinView.as_view(), name="join_classroom"),
    path("my-class", StudentClassroomListView.as_view(), name="student_classroom_list"),
    path("members/<int:classroom>", ClassroomStudentList.as_view(), name="classroom_classroom_list"),
    path("members/change/<int:pk>", ClassroomStudentModify.as_view(), name="classroom_classroom_list"),
    path("member-type/<int:classroom>", StudentTypeViewList.as_view(), name="student_type"),
    path("member-type/change/<int:pk>", StudentTypeViewDetail.as_view(), name="student_type_detail"),
]
