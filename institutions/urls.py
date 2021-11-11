from django.urls import path

from .views import *

app_name = "institutions"

urlpatterns = [
    path("create", InstitutionCreate.as_view(), name="institution_listcreate"),
    path("list", InstitutionListManage.as_view(), name="institution_listcreate"),
    path("verify", InstitutionVerificationView.as_view(), name="institution_verify"),
    path("verify/<int:pk>", InstitutionVerifyCheck.as_view(), name="institution_verify"),
    path("<int:pk>", InstitutionModify.as_view(), name="institution_modify"),
    path("subscribe", InstitutionPlanCreate.as_view(), name="institution_plan"),
]
