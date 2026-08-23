"""
Модели приложения Users: кастомный пользователь и история AI-запросов.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователей с email в качестве идентификатора."""

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и возвращает обычного пользователя."""
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт и возвращает суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с аутентификацией по email."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class AIRequest(models.Model):
    """
    История запроса пользователя на суммаризацию текста.
    Хранит исходный текст и полученный от AI-сервиса результат.
    Отдаётся пользователю через HistoryView, отфильтрованную по user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_requests")
    input_text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"AIRequest({self.user_id}, {self.created_at:%Y-%m-%d %H:%M})"
