from django.urls import path
from ..views.institution_views import *

urlpatterns = [
    # institution
    path("<int:pk>", InstitutionResourceListCreateView.as_view(), name="institution_resource_list"),
]
