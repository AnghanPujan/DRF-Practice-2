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
    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "password", "email", "role", "is_active"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user