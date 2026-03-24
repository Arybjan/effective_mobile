from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from .serializers import (
    UserProfileSerializer,
    RegisterSerializer,
    LoginSerializer,
    UpdateProfileSerializer,
)
from apps.access.models import Role
from .models import User, UserSession
from common.utils import check_password, generate_access_token

from datetime import datetime, timedelta, timezone


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        default_role = Role.objects.get(name="user")

        user = User.objects.create(
            first_name=serializer.validated_data(["first_name"]),
            last_name=serializer.validated_data(["last_name"]),
            middle_name=serializer.validated_data(["middle_name", ""]),
            email=serializer.validated_data(["email"]),
            password_hash=serializer.validated_data(["password"]),
            role=default_role,
        )

        return Response(
            {
                "message": "Пользователь успешно зарегистрирован.",
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"detail": "Неверный email или пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"detail": "Аккаунт деактивирован."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, user.password_hash):
            return Response(
                {"detail": "Неверный email или пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = generate_access_token(user.id, expires_minute=60)

        UserSession.objects.create(
            user=user,
            token=token,
            is_active=True,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=60),
        )
        return Response(
            {
                "message": "Успешный вход в систему",
                "access_token": token,
                "token_type": "Bearer",
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        token = request.auth

        UserSession.objects.filter(
            user=request.user,
            token=token,
            is_activate=True,
        ).update(is_active=False)

        return Response(
            {"message": "Вы успешно вышли из системы."},
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = UpdateProfileSerializer(
            isinstance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exeption=True)
        serializer.save()

        return Response(
            {
                "message": "Профиль обновлен",
                "user": UserProfileSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )


class SoftDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)
        user.save(update_fields=["is_active", "deleted_at", "updated_at"])

        UserSession.objects.filter(user=user, is_active=True).update(is_active=False)

        return Response({"message": "Аккаунт деактивирован"}, status=status.HTTP_200_OK)
