"""
Сериализаторы для модели Note.
"""
from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """Сериализатор заметки. id, created_at и updated_at — только для чтения."""
    class Meta:
        model = Note
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")