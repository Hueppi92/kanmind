from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import LoginSerializer, RegistrationSerializer, EmailCheckSerializer


class RegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'token': user.auth_token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': f'{user.first_name} {user.last_name}',
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': f"{user.first_name} {user.last_name}",
            },
            status=status.HTTP_200_OK
        )


class EmailCheckView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailCheckSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(get_user_model(), email__iexact=email)

     
        return Response(
            {
                'id': user.id,
                'email': email,
                'fullname': f"{user.first_name} {user.last_name}",
            },
            status=status.HTTP_200_OK
        )