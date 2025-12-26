from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')
    confirm_password=request.data.get('confirm_password')
    if password!=confirm_password:
        return Response({"message":"Passwords do not match"})
    if User.objects.filter(username=username):
        return Response({"message":"User Exists"})
    else:
        user= User.objects.create_user( 
            username=username,
            email=email,
            password=confirm_password)
        
    return Response({
        "message":"User Registered Successfully"},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username=request.data.get('username')
    password=request.data.get('password')

    user=authenticate(username=username, password=password)

    if user:
        refresh=RefreshToken.for_user(user)
        return Response(
            {"Message": "Login Successfull",
             "access": str(refresh.access_token),
             "refresh": str(refresh)
             },status=status.HTTP_200_OK)
    else:
        return Response({"Message":"Invalid User Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token=request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error':'Refresh token not given, required!'},
                 status=status.HTTP_400_BAD_REQUEST)
        token=RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {'message':'logout Successfull'},
            status=status.HTTP_205_RESET_CONTENT
        )
    except Exception:
        return Response(
            {"error":"Invalid Token"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
        


