"""
Корневая URL-конфигурация проекта config.
Объединяет маршруты админки, JWT-аутентификации, AI-сервиса, заметок и социальной аутентификации.
"""
from apps.users.views import EmailTokenObtainPairView
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import index


def health_check(request):
    """Эндпоинт проверки здоровья Django-сервиса."""
    return JsonResponse({"status": "healthy", "service": "django"})

urlpatterns = [
    # Главная страница
    path("", index),

    # Админка Django
    path("admin/", admin.site.urls),

    # JWT-аутентификация (получение и обновление токенов)
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Проверка здоровья сервиса
    path('api/health/', health_check, name='health'),

    # AI-сервис
    path("api/ai/", include("ai.urls")),

    # Notes API
    path("api/", include("apps.notes.urls")),

    # Социальная аутентификация
    path('social-auth/', include('social_django.urls', namespace='social')),
]