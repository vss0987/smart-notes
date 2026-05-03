"""
Модели приложения Notes.
"""
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Note(models.Model):
    """Модель заметки пользователя. Содержит заголовок, содержимое и временные метки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"