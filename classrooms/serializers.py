from rest_framework import serializers
from .models import *
from users.models import NewUser
import shortuuid


class ListClassroomSerializer(serializers.ModelSerializer):

    code = serializers.CharField(read_only=True, required=False)
    owner_first_name = serializers.CharField(source="owner.first_name", read_only=True)
    owner_last_name = serializers.CharField(source="owner.last_name", read_only=True)

    class Meta:
        model = Classroom
        fields = ("id", "name", "subject", "code", "owner_first_name", "owner_last_name", "status")


class ClassroomSerializer(serializers.ModelSerializer):

    code = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Classroom
        fields = ("id", "name", "subject", "code", "owner", "status")


class CreateClassroomSerializer(serializers.ModelSerializer):
    # code = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ("id", "name", "subject", "owner")


class MemberApplicationSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(many=True)
    classroom = serializers.StringRelatedField(many=True)

    class Meta:
        model = Student
        fields = ("id", "student", "classroom", "status")


class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResource
        fields = "__all__"


class ResourcesFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceFolder
        fields = "__all__"


class MemberSerializers(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source="student.first_name")
    student_last_name = serializers.CharField(source="student.last_name")

    class Meta:
        model = Student
        fields = ["classroom", "student_first_name", "student_last_name", "id", "status"]


class JoinClassroomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ClassroomListingField(serializers.RelatedField):
    def to_representation(self, value):
        return "%d/%s/%s/%s" % (value.id, value.name, value.description, value.section)


# class StudentClassroomSerializers(serializers.ModelSerializer):
#     classroom = ClassroomSerializer(many=False, read_only=True)

#     class Meta:
#         model = Student
#         fields = ["classroom"]


class StudentSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source="student.first_name")
    student_last_name = serializers.CharField(source="student.last_name")

    class Meta:
        model = Student
        fields = ["student_first_name", "student_last_name", "student"]


# List of Classroom members
class ClassroomStudentSerializer(serializers.ModelSerializer):
    members = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ("id", "name", "subject", "code", "owner", "members")


class ClassroomMembersSerializerModify(serializers.ModelSerializer):
    # members = StudentSerializer(many=True)
    # classroom_code = serializers.CharField(source="classroom.code")

    class Meta:
        model = Student
        fields = "__all__"


class JoinClassroomSerializer(serializers.ModelSerializer):
    classroom = serializers.SlugRelatedField(slug_field="code", queryset=Classroom.objects.all())

    class Meta:
        model = Student
        fields = ["id", "student", "status", "classroom"]


class ReturnClassroomByCode(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceUploadedFile
        fields = "__all__"


class FileQuillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomResourceQuillFile
        fields = "__all__"


class GetStudentsClassroomsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="classroom.name")
    subject = serializers.CharField(source="classroom.subject")
    id = serializers.CharField(source="classroom.id")
    description = serializers.CharField(source="classroom.description")
    classroom_adviser_f = serializers.CharField(source="classroom.owner.first_name")
    classroom_adviser_l = serializers.CharField(source="classroom.owner.last_name")

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "subject",
            "description",
            "classroom_adviser_f",
            "classroom_adviser_l",
        ]
