"""
Представления для аутентификации и регистрации.
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailTokenObtainPairSerializer, UserRegisterSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    """Эндпоинт для получения пары JWT-токенов по email и паролю."""
    serializer_class = EmailTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступна без авторизации — в отличие от остальных эндпоинтов проекта,
    у которых DEFAULT_PERMISSION_CLASSES = IsAuthenticated.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
