from rest_framework import generics, response, status
from rest_framework import pagination
from .models import *
from .serializers_copy import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework import generics
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class ModeratorInstitutionListCreate(generics.ListCreateAPIView):
    """Moderator List Create View"""

    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionSerializer

    def get_queryset(self):
        return Institution.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ModeratorInstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
    """This view will let User modify his institution"""

    permission_classes = [IsAuthenticated, IsInstitutionPaid, IsInstitutionVerified]
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionVerificationView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionVerificationSerializer

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


class InstitutionVerificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = InstitutionVerificationSerializer
    queryset = InstitutionVerification.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter(institution=Institution.objects.get(pk=self.kwargs["institution"]))

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class StaffList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionOwner, IsNotInstitutionOwner]
    serializer_class = StaffSerializer

    def get_queryset(self):
        return Staff.objects.filter(institution=self.kwargs["institution"])

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]), user=self.request.user)


# Untested for other account
class StaffTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = StaffTypeSerializer
    queryset = StaffType.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class StaffTypeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionOwner]
    serializer_class = StaffTypeSerializer

    def get_queryset(self):
        result = StaffType.objects.filter(custom_Type_For=self.kwargs["institution"]) | StaffType.objects.filter(
            custom_Type_For__isnull=True
        )
        return result

    def perform_create(self, serializer):
        serializer.save(custom_Type_For=Institution.objects.get(pk=self.kwargs["institution"]))


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class InstitutionSearchList(generics.ListAPIView):
    """Generic List View for Institution that allows searching and has pagination"""

    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionSerializer
    queryset = Institution.publicProduct.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "address", "owner__username"]


# Institution Staff list view please
class StaffInstitutionList(generics.ListAPIView):
    """This view list all the staff's Institution"""

    permission_classes = [IsAuthenticated]
    serializer_class = StaffInstitutionSerializer

    def get_queryset(self):
        return Staff.objects.filter(user=self.request.user)
