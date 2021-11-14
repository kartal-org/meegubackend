from rest_framework import serializers
from .models import *


class AdviserClassroomSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.full_name", read_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Classroom
        fields = ["id", "name", "description", "privacy", "code", "subject", "cover", "owner"]


class JoinClassroomSerializer(serializers.ModelSerializer):
    classroom = serializers.SlugRelatedField(slug_field="code", queryset=Classroom.objects.all())
    name = serializers.CharField(source="classroom.name", read_only=True)
    description = serializers.CharField(source="classroom.description", read_only=True)
    id = serializers.CharField(source="classroom.id", read_only=True)
    cover = serializers.FileField(source="classroom.cover", read_only=True)
    owner = serializers.CharField(source="classroom.owner.full_name", read_only=True)
    subject = serializers.CharField(source="classroom.subject", read_only=True)

    class Meta:
        model = Student
        fields = ["id", "status", "classroom", "name", "description", "cover", "owner", "subject"]


class StudentClassroomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="classroom.code")
    name = serializers.CharField(source="classroom.name")
    description = serializers.CharField(source="classroom.description")
    id = serializers.CharField(source="classroom.id")
    cover = serializers.FileField(source="classroom.cover")
    owner = serializers.CharField(source="classroom.owner.full_name")
    subject = serializers.CharField(source="classroom.subject")

    class Meta:
        model = Student
        fields = ["id", "status", "code", "name", "description", "cover", "owner", "subject", "classroom"]


class ClassroomStudentSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name")
    image = serializers.FileField(source="user.image")
    fullname = serializers.CharField(source="user.full_name")

    class Meta:
        model = Student
        fields = ["id", "status", "fullname", "image", "role"]


class StudentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = ["id", "name", "description", "permissions", "custom_Type_For"]
