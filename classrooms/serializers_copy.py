from rest_framework import serializers
from .models import *


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class ClassroomListSerializer(serializers.ModelSerializer):
    classrooms = ClassroomSerializer(read_only=True, many=True)

    class Meta:
        model = ClassroomMember
        fields = ["classrooms"]


# class AdviserClassroomSerializer(serializers.ModelSerializer):
#     # owner = serializers.CharField(source="owner.full_name", read_only=True)

#     class Meta:
#         model = Classroom
#         fields = "__all__"
#         extra_kwargs = {"code": {"read_only": True}}

#     def create(self, validated_data):
#         print(self)
#         print(validated_data)
#         return Classroom(validated_data)


# class JoinClassroomSerializer(serializers.ModelSerializer):
#     classroom = serializers.SlugRelatedField(slug_field="code", queryset=Classroom.objects.all())
#     name = serializers.CharField(source="classroom.name", read_only=True)
#     description = serializers.CharField(source="classroom.description", read_only=True)
#     id = serializers.CharField(source="classroom.id", read_only=True)
#     cover = serializers.FileField(source="classroom.cover", read_only=True)
#     # owner = serializers.CharField(source="classroom.owner.full_name", read_only=True)
#     subject = serializers.CharField(source="classroom.subject", read_only=True)

#     class Meta:
#         model = ClassroomMember
#         fields = ["id", "status", "classroom", "name", "description", "cover", "subject"]


# class StudentClassroomSerializer(serializers.ModelSerializer):
#     code = serializers.CharField(source="classroom.code")
#     name = serializers.CharField(source="classroom.name")
#     description = serializers.CharField(source="classroom.description")
#     id = serializers.CharField(source="classroom.id")
#     cover = serializers.FileField(source="classroom.cover")
#     # owner = serializers.CharField(source="classroom.owner.full_name")
#     subject = serializers.CharField(source="classroom.subject")

#     class Meta:
#         model = ClassroomMember
#         fields = ["id", "status", "code", "name", "description", "cover", "subject", "classroom"]


# class ClassroomStudentSerializer(serializers.ModelSerializer):
#     # role = serializers.CharField(source="role.name")
#     image = serializers.FileField(source="user.image", read_only=True)
#     name = serializers.CharField(source="user.full_name", read_only=True)
#     username = serializers.CharField(source="user.username", read_only=True)

#     class Meta:
#         model = ClassroomMember
#         fields = ["id", "status", "name", "image", "username"]
