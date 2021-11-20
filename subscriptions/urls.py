from django.urls import path

from .views import *

urlpatterns = [
    path("classroom", ClassroomPlanListView.as_view(), name="classroom_plan_list"),
    path("institution", InstitutionPlanListView.as_view(), name="institution_plan_list"),
    path("buy/classroom/<int:classroom>", ClassroomSubscriptionListCreateView.as_view(), name="classroom_buy"),
    path("buy/institution/<int:institution>", InstitutionSubscriptionListCreateView.as_view(), name="institution_buy"),
]
