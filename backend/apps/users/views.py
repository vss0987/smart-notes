"""
Представления для аутентификации.
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    """Эндпоинт для получения пары JWT-токенов по email и паролю."""
    serializer_class = EmailTokenObtainPairSerializer