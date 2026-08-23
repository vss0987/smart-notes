"""
Представления API для обработки запросов.
"""
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.models import AIRequest
from apps.users.serializers import AIRequestSerializer

from .services import summarize_text, AIServiceUnavailable


class SummarizeView(APIView):
    """
    Эндпоинт для суммаризации текста.
    Доступен только аутентифицированным пользователям.
    Принимает POST-запрос с полем 'text', возвращает результат суммаризации
    и сохраняет запрос в историю текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response({"error": "Text is required"}, status=400)

        try:
            result = summarize_text(text)
        except AIServiceUnavailable:
            return Response(
                {"error": "AI-сервис временно недоступен. Попробуйте позже."},
                status=503,
            )

        AIRequest.objects.create(
            user=request.user,
            input_text=text,
            summary=result,
        )

        return Response(result)


class HistoryView(ListAPIView):
    """
    История суммаризаций текущего пользователя, от новых к старым.

    get_queryset фильтрует по request.user — это и есть защита от чужих
    данных: пользователь физически не может получить чужие записи,
    даже зная чужой id, потому что запрос к БД изначально их не включает.
    """
    serializer_class = AIRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIRequest.objects.filter(user=self.request.user).order_by("-created_at")
