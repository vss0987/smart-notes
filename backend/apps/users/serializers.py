"""
Сериализаторы для JWT-аутентификации, регистрации и истории AI-запросов.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AIRequest

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения JWT-токенов по email вместо username."""
    username_field = "email"


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация нового пользователя по email и паролю.
    Пароль проверяется через стандартные Django-валидаторы
    (AUTH_PASSWORD_VALIDATORS из settings.py) и никогда не возвращается обратно.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )


class AIRequestSerializer(serializers.ModelSerializer):
    """Одна запись истории суммаризаций — только для чтения."""

    class Meta:
        model = AIRequest
        fields = ("id", "input_text", "summary", "created_at")
        read_only_fields = fields
