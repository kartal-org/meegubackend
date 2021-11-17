# from django.views import generic
# from rest_framework import generics, response, status
# from .models import *
# from .serializers import *
# from rest_framework.permissions import IsAuthenticated
# from .permissions import *
# from rest_framework.views import APIView
# from rest_framework import viewsets, filters, generics, permissions
# from django.shortcuts import get_list_or_404, get_object_or_404
# from rest_framework.parsers import MultiPartParser, FormParser

# from django.db.models.functions import Cast
# from django.db.models import Sum, IntegerField
# from django.contrib.postgres.fields.jsonb import KeyTextTransform


# class InstitutionListManage(generics.ListAPIView):
#     """This view will let User see all his Institution"""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ModifiedInstitutionSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return InstitutionVerification.objects.filter(institution__owner=user)


# class InstitutionCreate(generics.CreateAPIView):
#     """This view will let User create his Institution"""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CreateInstitutionSerializer

#     def perform_create(self, serializer):
#         owner = self.request.user
#         serializer.save(owner=owner)


# class InstitutionModify(generics.RetrieveUpdateDestroyAPIView):
#     """This view will let User create his classrooms"""

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = InstitutionSerializer
#     lookup_field = "pk"
#     queryset = Institution.objects.all()


# class InstitutionVerificationView(generics.CreateAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = InstitutionVerificationSerializer


# class InstitutionVerifyCheck(generics.RetrieveUpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = InstitutionVerificationSerializer

#     def get_object(self):
#         queryset = InstitutionVerification.objects.all()
#         institution = self.kwargs["pk"]
#         obj = get_object_or_404(queryset, institution=institution)
#         return obj


# class InstitutionPlanCreate(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = InstitutionSubscriptionSerializer


# class InstitutionResourceCreate(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     # serializer_class = some serializer
#     # def create(self, request, *args, **kwargs):
#     #     institution = self.request.data["institution"]
#     #     1. aggregate all subscription plan's resource Limit
#     # 2. count all the resource under specific institution
#     #     limitationResource = InstitutionSubscription.objects.filter(institution=13).annotate(resource_limit=Cast(KeyTextTransform('resourceNum', 'plan__limitations'), IntegerField())).aggregate(Sum('resource_limit'))
#     #     limitation=limitationResource['resource_limit__sum']
#     #     resourceTotal = InstitutionResource.objects.filter(institution=13).count()

#     #     if resourceTotal >= limitation:
#     #       print("captured")
#     #       return response.Response(
#     #             {"error": "You reach your limit of resource number, subscribe to a new plan"},
#     #             status=status.HTTP_403_FORBIDDEN,
#     #         )
#     #     else:
#     #       proceed creation
#     pass
