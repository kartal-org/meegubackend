from django.views import generic
from rest_framework import generics, response, status

from .permissions import IsNotFirstClassroom
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class ClassroomPlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.classroomPlans.all()


class InstitutionPlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.institutionPlans.all()


class ClassroomSubscribeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotFirstClassroom]
    serializer_class = BuySubscriptionSerializer
