"""
Представления API для обработки запросов.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import summarize_text


class SummarizeView(APIView):
    """
    Эндпоинт для суммаризации текста.
    Доступен только аутентифицированным пользователям.
    Принимает POST-запрос с полем 'text', возвращает результат суммаризации.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Обрабатывает POST-запрос, извлекает текст и возвращает суммаризацию."""
        text = request.data.get("text")

        if not text:
            return Response({"error": "Text is required"}, status=400)

        result = summarize_text(text)

        return Response(result)