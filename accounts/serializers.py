from rest_framework import serializers
from .models import CustomUser, StudentProfile, TeacherProfile, AdminProfile

# Serializer for creating a user without nested profiles
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'default': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'student'),
            is_active=validated_data.get('is_active', True),
        )
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["roll", "course", "year", "section"]

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ["subject", "department", "designation"]

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ["office", "position"]


class CustomUserSerializer(serializers.ModelSerializer):
    # Make nested profiles write_only so they are used only for create/update
    studentprofile = StudentProfileSerializer(required=False, write_only=True)
    teacherprofile = TeacherProfileSerializer(required=False, write_only=True)
    adminprofile = AdminProfileSerializer(required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "password", "email", "role", "is_active",
            "studentprofile", "teacherprofile", "adminprofile"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role = validated_data.get("role")
        student_data = validated_data.pop("studentprofile", None)
        teacher_data = validated_data.pop("teacherprofile", None)
        admin_data = validated_data.pop("adminprofile", None)

        # Create the user
        user = CustomUser.objects.create_user(**validated_data)

        # Create the corresponding profile based on role
        if role == "student" and student_data:
            StudentProfile.objects.create(user=user, **student_data)
        elif role == "teacher" and teacher_data:
            TeacherProfile.objects.create(user=user, **teacher_data)
        elif role == "admin" and admin_data:
            AdminProfile.objects.create(user=user, **admin_data)
        return user
 