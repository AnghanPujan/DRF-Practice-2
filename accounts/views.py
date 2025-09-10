from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, CustomUserSerializer
from rest_framework import generics
from .models import CustomUser
from .authentication import IsAdmin, IsSuperAdmin
import json
class LoginAPIView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"msg": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {"msg": "This account is inactive. Contact admin."},
                    status=status.HTTP_403_FORBIDDEN
                )

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "role": getattr(user, "role", ""),
                "is_superuser": user.is_superuser,
                "message": "Login successful",
                "created": created,
            }, status=status.HTTP_200_OK)

        return Response(
            {"msg": "Invalid Username OR Password !"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class RegisterAPIView(APIView):
    authentication_classes = []  
    permission_classes = [IsAdmin] 

    
    

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class SuperAdminDashboard(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)

        all_users = CustomUser.objects.all()
        total_users = all_users.count()
        active_users = all_users.filter(is_active=True).count()
        inactive = total_users - active_users

        serializer = CustomUserSerializer(all_users, many=True)

        return Response({
            'total_users': total_users,
            "active_users": active_users,
            "inactive_users": inactive,
            "all_users": serializer.data
        })

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "user": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User partially updated successfully",
                "user": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        if user.role == 'super admin':
            return Response(
                {"message": "Cannot delete a super admin."},
                status=status.HTTP_403_FORBIDDEN
            )

        user.delete()  
        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )