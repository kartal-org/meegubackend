from django.urls import path
from . import views
from .views import * 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   
    path('dashboard/', views.home, name="dashboard"),
    path('institutionVerify/<str:pk_instv>/', views.institutionVerify, name="verifyPage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

