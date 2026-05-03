"""
Pydantic-схемы для запросов и ответов API.
"""
from pydantic import BaseModel


class SummaryRequest(BaseModel):
    """Тело запроса на суммаризацию."""
    text: str


class SummaryResponse(BaseModel):
    """Тело ответа с результатом суммаризации."""
    summary: str