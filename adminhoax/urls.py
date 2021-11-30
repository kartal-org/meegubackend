from django.urls import path
from . import views
from .views import * 

urlpatterns = [   
    path('dashboard/', views.home, name="dashboard"),
]

