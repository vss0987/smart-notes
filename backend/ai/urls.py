"""
Маршрутизация URL для приложения.
"""
from django.urls import path
from .views import SummarizeView, HistoryView

urlpatterns = [
    # POST-эндпоинт для суммаризации текста
    path("summarize/", SummarizeView.as_view()),
    # GET-эндпоинт истории суммаризаций текущего пользователя
    path("history/", HistoryView.as_view()),
]
