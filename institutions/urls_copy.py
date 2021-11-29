from django.urls import path

from .views_copy import *

app_name = "institutions"

urlpatterns = [
    path("", ModeratorInstitutionCreate.as_view(), name="institution_create"),
    path("staff/list", StaffInstitutionList.as_view(), name="staff_institution_list"),
    path("moderator/list", ModeratorInstitutionList.as_view(), name="moderator_institution_list"),
    path("change/<int:pk>", ModeratorInstitutionDetail.as_view(), name="institution_detail"),
    path("verify/<int:institution>", InstitutionVerificationView.as_view(), name="institution_verify"),
    path("verify/change/<int:pk>", InstitutionVerificationDetailView.as_view(), name="institution_verify_update"),
    path("department/<int:institution>", DepartmentListCreate.as_view(), name="department_list"),
    path("department/change/<int:pk>", DepartmentDetail.as_view(), name="department_detail"),
    path("staff/change/<int:pk>", StaffDetail.as_view(), name="staff_detail"),
    path("staff/<int:institution>", StaffList.as_view(), name="staff_list"),
    path("staff-type/change/<int:pk>", StaffTypeDetail.as_view(), name="staff_type_detail"),
    path("staff-type/<int:institution>", StaffTypeList.as_view(), name="staff_type_list"),
    # Staff's
    path("sharedInstitution", StaffInstitutionList.as_view(), name="staff_institution_list"),
    # Search and Filtering
    path("search", InstitutionSearchList.as_view(), name="institution_search_list"),
]
