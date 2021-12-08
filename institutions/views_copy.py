from rest_framework import generics, response, status
from rest_framework import pagination
from .models import *
from .serializers_copy import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from .permissions_copy import *
from rest_framework import generics
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter


class InstitutionCreateView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionSerializer


class InstitutionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionListSerializer

    def get_queryset(self):
        return Staff.objects.filter(user=self.request.user)


class OwnerInstitutionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionListSerializer

    def get_queryset(self):
        return Staff.objects.filter(user=self.request.user, type__name="Admin")


class StaffInstitutionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionListSerializer

    def get_queryset(self):
        return Staff.objects.filter(user=self.request.user).exclude(type__name="Admin")


class InstitutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsInstitutionCreator]
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class StaffListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StaffSerializer
    filter_backends = [SearchFilter]
    search_fields = ["department__id", "institution__slug"]
    queryset = Staff.objects.all()


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsPermitStaffEdit]
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class StaffTypeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StaffTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["custom_Type_For__id"]
    queryset = StaffType.objects.all()


class StaffTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StaffTypeSerializer
    queryset = StaffType.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionVerificationView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionVerificationSerializer


class DepartmentListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter(institution=Institution.objects.get(pk=self.kwargs["institution"]))

    def perform_create(self, serializer):
        serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


class DepartmentWhereStaffList(generics.ListAPIView):
    """List of Department relevant to staff"""

    permission_classes = [IsAuthenticated]
    serializer_class = StaffsDepartmentSerializer

    def get_queryset(self):
        return Staff.objects.filter(user=self.request.user)


# class DepartmentStaffListCreate(generics.ListCreateAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#     serializer_class = DepartmentSerializer

#     def get_queryset(self):
#         return Department.objects.filter(institution=Institution.objects.get(pk=self.kwargs["institution"]))

#     def perform_create(self, serializer):
#         serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


# class DepartmentStaffListCreate(generics.ListCreateAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#     serializer_class = StaffSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ["department__id"]
#     queryset = Staff.objects.all()

# def get_queryset(self):
#     return Staff.objects.filter(department=Institution.objects.get(pk=self.kwargs["institution"]))

# def perform_create(self, serializer):
#     serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


# Creation of custom staff type for later

# class ModeratorInstitutionCreate(generics.CreateAPIView):
#     """Moderator List Create View"""

#     permission_classes = [IsAuthenticated]
#     serializer_class = InstitutionSerializer

#     # def get_queryset(self):
#     #     return Institution.objects.filter(owner=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class ModeratorInstitutionDetail(generics.RetrieveUpdateDestroyAPIView):
#     """This view will let User modify his institution"""

#     permission_classes = [IsAuthenticated, IsInstitutionPaid, IsInstitutionVerified]
#     serializer_class = InstitutionSerializer
#     queryset = Institution.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class ModeratorInstitutionList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = InstitutionByStaffSerializer

#     def get_queryset(self):
#         return Staff.objects.filter(user=self.request.user, type__name="Creator")

#     # def list(self, request, *args, **kwargs):
#     #     queryset = self.filter_queryset(self.get_queryset())

#     #     page = self.paginate_queryset(queryset)
#     #     if page is not None:
#     #         serializer = self.get_serializer(page, many=True)
#     #         return self.get_paginated_response(serializer.data)

#     #     serializer = self.get_serializer(queryset, many=True)
#     #     breakpoint()
#     #     return response.Response(serializer.data)


# class StaffInstitutionList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = InstitutionByStaffSerializer

#     def get_queryset(self):
#         return Staff.objects.filter(user=self.request.user).exclude(type__name="Creator")


# class InstitutionVerificationView(generics.CreateAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated]
#     serializer_class = InstitutionVerificationSerializer

#     def perform_create(self, serializer):
#         serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]))


# class InstitutionVerificationDetailView(generics.RetrieveUpdateDestroyAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated, IsInstitutionOwner]
#     serializer_class = InstitutionVerificationSerializer
#     queryset = InstitutionVerification.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [IsAuthenticated, IsInstitutionOwner]
#     serializer_class = DepartmentSerializer
#     queryset = Department.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsInstitutionOwner]
#     serializer_class = StaffSerializer
#     queryset = Staff.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class StaffList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated, IsInstitutionOwner, IsNotInstitutionOwner]
#     serializer_class = StaffSerializer

#     def get_queryset(self):
#         return Staff.objects.filter(institution=self.kwargs["institution"])

#     def perform_create(self, serializer):
#         serializer.save(institution=Institution.objects.get(pk=self.kwargs["institution"]), user=self.request.user)


# # Untested for other account
# class StaffTypeDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsInstitutionOwner]
#     serializer_class = StaffTypeSerializer
#     queryset = StaffType.objects.all()

#     def destroy(self, *args, **kwargs):
#         serializer = self.get_serializer(self.get_object())
#         super().destroy(*args, **kwargs)
#         return response.Response(serializer.data, status=status.HTTP_200_OK)


# class StaffTypeList(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated, IsInstitutionOwner]
#     serializer_class = StaffTypeSerializer

#     def get_queryset(self):
#         result = StaffType.objects.filter(custom_Type_For=self.kwargs["institution"]) | StaffType.objects.filter(
#             custom_Type_For__isnull=True
#         )
#         return result

#     def perform_create(self, serializer):
#         serializer.save(custom_Type_For=Institution.objects.get(pk=self.kwargs["institution"]))


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = "page_size"
#     max_page_size = 10


# class InstitutionSearchList(generics.ListAPIView):
#     """Generic List View for Institution that allows searching and has pagination"""

#     permission_classes = [IsAuthenticated]
#     serializer_class = InstitutionSerializer
#     queryset = Institution.publicProduct.all()
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ["name", "address", "owner__username"]


# # # Institution Staff list view please
# # class StaffInstitutionList(generics.ListAPIView):
# #     """This view list all the staff's Institution"""

# #     permission_classes = [IsAuthenticated]
# #     serializer_class = StaffInstitutionSerializer

# #     def get_queryset(self):
# #         return Staff.objects.filter(user=self.request.user)
