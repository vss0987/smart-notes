"""
Модели для хранения AI-запросов и ответов.
"""
from django.db import models
from ..notes.models import Note


class AIRequest(models.Model):
    """
    Модель AI-запроса к заметке.
    Хранит тип запроса, переданный промпт и полученный ответ от AI-сервиса.
    """
    SUMMARY = "summary"
    TODO = "todo"
    TAGS = "tags"
    QUESTION = "question"

    REQUEST_TYPES = [
        (SUMMARY, "Summary"),
        (TODO, "Todo"),
        (TAGS, "Tags"),
        (QUESTION, "Question"),
    ]

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name="ai_requests"
    )
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPES
    )
    prompt = models.TextField()
    response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_type} for note {self.note_id}"