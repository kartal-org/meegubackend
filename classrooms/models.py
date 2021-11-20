from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE, SET_NULL
from institutions.models import Institution
from products.models import Product
from members.models import BaseMember, BaseMemberType


class Classroom(Product):
    code = models.CharField(max_length=8, unique=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)


class StudentType(BaseMemberType):
    custom_Type_For = models.ForeignKey(Classroom, on_delete=CASCADE, null=True, blank=True)


class Student(BaseMember):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="members")
    role = models.ForeignKey(StudentType, on_delete=SET_NULL, null=True, blank=True)  # should remove this

    class Meta:
        unique_together = ["user", "classroom"]
