"""
Точка входа для запуска FastAPI-приложения через Uvicorn.
Запускает сервер на 127.0.0.1:8001 с автоматической перезагрузкой при изменениях.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)