import re
from django.shortcuts import render
from .serializers import UserSerializer, UserDetail, ChangePasswordSerializer, UpdateUserSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from  rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .utils import jwt_decode_handler
from django.contrib.auth import get_user_model, password_validation


User = get_user_model()

# Create your views here.

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        data  = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            data = dict(serializer.data)
            data.pop('password')

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = super().post( request, *args, **kwargs)

        data = data.data

        access_token = jwt_decode_handler(data.get("access"))
        user = User.objects.filter(email=access_token.get("email")).first()

        if not user:
            return Response({"error":True, "message":"No such user!"}, status=status.HTTP_404_NOT_FOUND)


        serializer = UserDetail(user)

        data["user"] = serializer.data

        return Response(data)    



class RefreshTokenView(TokenRefreshView):


    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)

        data = data.data

        return Response(data)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated ,)
    serializer_class = ChangePasswordSerializer

class UpdateUserView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated ,)
    serializer_class = UpdateUserSerializer    