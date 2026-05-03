"""
Маршрутизация URL для приложения.
"""
from django.urls import path
from .views import SummarizeView

urlpatterns = [
    # POST-эндпоинт для суммаризации текста
    path("summarize/", SummarizeView.as_view()),
]