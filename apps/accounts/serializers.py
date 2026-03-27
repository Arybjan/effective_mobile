from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_repeat = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Пароли не совпадают но но но")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_active", "created_at", "updated_at")


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "middle_name", "email")

    def validate_email(self, value):
        user = self.instans
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise ValueError("Этот email уже занят")

        return value
