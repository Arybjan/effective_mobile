from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from .serializers import UserProfileSerializer, RegisterSerializer
from apps.access.models import Role
from .models import User, UserSession


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
    
