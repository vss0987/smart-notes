"""
Модуль безопасности. Проверка внутреннего токена для защиты эндпоинтов.
"""
import os
from fastapi import Header, HTTPException

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")

def verify_internal_token(x_internal_token: str = Header(...)):
    """
    Проверяет заголовок X-Internal-Token.
    Если токен не совпадает — возвращает 401.
    """
    if x_internal_token != INTERNAL_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid internal token")