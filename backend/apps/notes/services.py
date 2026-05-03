"""
Бизнес-логика для работы с заметками.
"""
from .models import Note


def create_note(*, user, title: str, content: str) -> Note:
    """Создаёт новую заметку для указанного пользователя."""
    return Note.objects.create(
        user=user,
        title=title,
        content=content
    )