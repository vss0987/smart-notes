"""
Сервисный слой для взаимодействия с внутренним AI-сервисом.
Содержит функцию отправки текста на суммаризацию.
"""
import os
import httpx

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001")


class AIServiceUnavailable(Exception):
    """AI-сервис недоступен или ответил ошибкой."""
    pass


def summarize_text(text: str) -> str:
    """
    Отправляет текст в AI-сервис для суммаризации.

    Args:
        text: Исходный текст для обработки.

    Returns:
        Строка с результатом суммаризации.

    Raises:
        RuntimeError: Если не задан INTERNAL_API_TOKEN.
        AIServiceUnavailable: При сетевых ошибках, таймауте или ошибке AI-сервиса.
    """
    if not INTERNAL_API_TOKEN:
        raise RuntimeError("INTERNAL_API_TOKEN is not set")

    try:
        response = httpx.post(
            f"{AI_SERVICE_URL}/summarize",
            json={"text": text},
            headers={
                "X-Internal-Token": INTERNAL_API_TOKEN
            },
            # Внутри ai_service таймаут к YandexGPT — 60 секунд, поэтому
            # здесь таймаут должен быть не меньше, иначе Django обрывает
            # запрос раньше, чем ai_service вообще получит ответ.
            timeout=65,
        )
        response.raise_for_status()

    except httpx.TimeoutException as exc:
        raise AIServiceUnavailable("AI-сервис не ответил вовремя") from exc
    except httpx.HTTPStatusError as exc:
        raise AIServiceUnavailable(f"AI-сервис вернул ошибку: {exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        raise AIServiceUnavailable("Не удалось подключиться к AI-сервису") from exc

    return response.json()["summary"]
