from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class LoginAPIView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Please provide both username and password"},
                            status=status.HTTP_400_BAD_REQUEST)
        print("username :- ",username)
        print("password :- ",password)

        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate the token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                    'token': token.key,
                    'username' : user.username,
                    'message': "Login successful",
                    'created': created
                },
                status=status.HTTP_200_OK
                )
        return Response({
                'msg' : 'Invalid Username OR Password !'
            },
            status=status.HTTP_404_NOT_FOUND
        )

class RegisterAPIView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny] 

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