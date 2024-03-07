from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

from auth.models import User
from auth.serializers import UserSerializer
from auth.tokens import BearerTokenAuthentication


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        result = super(RegisterAPIView, self).create(request, *args, **kwargs)

        user = User.objects.get(email=request.data['email'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"success": True, "message": "Success", "token": token.key}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)
