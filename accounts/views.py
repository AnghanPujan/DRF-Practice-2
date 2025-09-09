from django.shortcuts import render
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

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class SuperAdminDashboard(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        all_users = CustomUser.objects.all()
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True)
        inactive = total_users - len(active_users)

        serializer = CustomUserSerializer(all_users, many=True)
        print(json.dumps(serializer.data))
    
        return Response({
            'total_users' : total_users,
            "active_users" : len(active_users),
            "inactive users" : inactive,
            "all_users" : serializer.data
        })  