from django.views import generic
from rest_framework import generics, response, status

from .permissions import IsNotFirstClassroom
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters, generics, permissions
from django.shortcuts import get_list_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from classrooms.models import Classroom
from institutions.models import Institution

# Create your views here.


class ClassroomPlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer
    # queryset = Plan.classroomPlans.all()

    def get_queryset(self):
        subscriptionList = ClassroomSubscription.objects.filter(classroom__creator=self.request.user)
        if subscriptionList:
            if "Classroom Basic" in [o.plan.name for o in subscriptionList]:
                return Plan.classroomPlans.exclude(name="Classroom Basic")
        return Plan.classroomPlans.all()


class InstitutionPlanListView(generics.ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        # print(Plan.institutionPlans.all())
        # breakpoint()
        # subscriptionList = get_list_or_404(InstitutionSubscription, institution__creator=self.request.user)
        if "Institution Basic" in [
            o.plan.name for o in InstitutionSubscription.objects.filter(institution__creator=self.request.user)
        ]:
            return Plan.institutionPlans.exclude(name="Institution Basic")
        return Plan.institutionPlans.all()


class ClassroomSubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuySubscriptionSerializer

    def get_queryset(self):
        return ClassroomSubscription.objects.filter(classroom=self.kwargs.get("classroom"))

    def perform_create(self, serializer):
        serializer.save(classroom=Classroom.objects.get(pk=self.kwargs["classroom"]))


class InstitutionSubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionSubscriptionSerializer

    def get_queryset(self):
        return InstitutionSubscription.objects.filter(institution=self.kwargs.get("institution"))

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))
