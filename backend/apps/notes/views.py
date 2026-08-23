"""
Представления для CRUD-операций с заметками.
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwner
from .selectors import get_user_notes
from .services import create_note


class NoteViewSet(ModelViewSet):
    """
    ViewSet для управления заметками.
    Доступен только аутентифицированным пользователям и только к своим заметкам.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает заметки текущего пользователя."""
        return get_user_notes(user=self.request.user)

    def perform_create(self, serializer):
        """
        Создаёт заметку, привязывая её к текущему пользователю.

        Важно: результат create_note() присваивается serializer.instance —
        без этого DRF после perform_create() пытается сериализовать
        serializer.validated_data (обычный dict без id/created_at/updated_at,
        так как это read-only поля) вместо реальной модели, и ответ клиенту
        получается битым или падает с ошибкой.
        """
        note = create_note(
            user=self.request.user,
            title=serializer.validated_data["title"],
            content=serializer.validated_data["content"],
        )
        serializer.instance = note
