"""
Сериализаторы для JWT-аутентификации.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения JWT-токенов по email вместо username."""
    username_field = "email"