"""
Корневые представления проекта.
"""
from django.shortcuts import render


def index(request):
    """Отдаёт главную страницу (index.html)."""
    return render(request, "index.html")