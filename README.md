# Smart Notes AI

Smart Notes AI — это веб-приложение для суммаризации текстовых заметок с использованием искусственного интеллекта.

Система позволяет пользователям отправлять длинные тексты и получать их краткое содержание, сгенерированное AI-моделью.

Проект демонстрирует использование микросервисной архитектуры, Python-фреймворков и контейнеризированной инфраструктуры.

---

# Возможности

* суммаризация текста с использованием AI
* аутентификация пользователей (JWT)
* хранение персональной истории запросов
* REST API backend
* микросервисная архитектура
* запуск через Docker

---

# Архитектура

Приложение состоит из трёх сервисов:

Frontend (Nginx + HTML/JS)
Django Backend (REST API)
AI Service (FastAPI)

```
Frontend
   │
   ▼
Nginx
   │
   ▼
Django REST API
   │
   ▼
FastAPI AI Service
   │
   ▼
YandexGPT API
```

Backend отвечает за аутентификацию пользователей, обработку запросов и хранение данных.

AI-сервис отвечает за взаимодействие с внешним AI-провайдером.

---

# Технологический стек

Backend

* Python
* Django
* Django REST Framework
* JWT Authentication

AI сервис

* FastAPI
* Uvicorn
* httpx

Frontend

* HTML
* CSS
* JavaScript (Fetch API)

Инфраструктура

* Docker
* Docker Compose
* Nginx

База данных

* SQLite (может быть заменена на PostgreSQL)

---

# API endpoints

Аутентификация

POST /api/users/register/
POST /api/token/

AI

POST /api/ai/summarize/
GET /api/ai/history/

Проверка состояния сервера

GET /api/health/

---

# Запуск проекта

Клонировать репозиторий:

```
git clone https://github.com/vss0987/smart-notes
cd smart-notes
```

Создать файл .env в корне проекта:

YANDEX_API_KEY=сюда ключ без кавычек

YANDEX_FOLDER_ID=сюда id без кавычек

YANDEX_API_KEY и YANDEX_FOLDER_ID можно получить бесплатно на [yandex](https://yandex.cloud/ru)

INTERNAL_TOKEN=super-secret-internal-token - можно так и оставить

INTERNAL_API_TOKEN=super-secret-internal-token - это тоже

#Django secret key
SECRET_KEY="ключ django из settings"

Создать docker-compose.yml
```
services:
  frontend:
    image: sergeyv1987/smart-notes-frontend:latest
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    image: sergeyv1987/smart-notes-backend:latest
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - ai_service

  ai_service:
    image: sergeyv1987/smart-notes-ai_service:latest
    ports:
      - "8001:8001"
    env_file:
      - .env
```

Запустить контейнеры:

```
docker-compose up --build
```

Открыть в браузере:

```
http://localhost:3000
```

---

# Цели проекта

Проект демонстрирует:

* разработку REST API на Django REST Framework
* интеграцию AI-провайдеров
* проектирование микросервисной архитектуры
* контейнеризацию приложений с помощью Docker
* реализацию аутентификации и хранения пользовательских данных
