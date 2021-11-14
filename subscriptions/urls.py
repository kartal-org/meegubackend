from django.urls import path

from .views import *

urlpatterns = [
    path("classroom", ClassroomPlanListView.as_view(), name="classroom_plan_list"),
    path("institution", InstitutionPlanListView.as_view(), name="institution_plan_list"),
    path("buy/classroom", ClassroomSubscribeCreateView.as_view(), name="classroom_buy"),
]
