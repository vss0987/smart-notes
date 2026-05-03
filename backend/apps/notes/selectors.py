"""
Селекторы для получения заметок из БД.
"""
from .models import Note


def get_user_notes(*, user):
    """Возвращает все заметки пользователя."""
    return Note.objects.filter(user=user)


def get_user_note_by_id(*, user, note_id: int):
    """Возвращает конкретную заметку пользователя по ID."""
    return Note.objects.get(id=note_id, user=user)