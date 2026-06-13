# Habit Tracker API

Backend-часть SPA-приложения для трекинга полезных привычек по мотивам книги «Атомные привычки» Джеймса Клира.[web:454]  
Проект реализован на Django REST Framework с интеграцией Celery, Redis и Telegram-бота для напоминаний.[web:453][web:455]

---

## Основной функционал

- Регистрация и авторизация пользователей по JWT (Simple JWT).
- CRUD для привычек текущего пользователя.
- Публичные привычки, доступные для просмотра всем.
- Валидация привычек по бизнес-правилам:
  - длительность не более 120 секунд;
  - периодичность от 1 до 7 дней;
  - нельзя одновременно указать вознаграждение и связанную привычку;
  - только «приятные» привычки могут быть связаны как вознаграждение.
- Пагинация списка привычек (5 объектов на страницу, формат `count/next/previous/results`).]
- Отправка напоминаний о привычках в Telegram по расписанию (Celery + Redis + django-celery-beat).

---

## Технологии

- **Backend**: Django 6, Django REST Framework.
- **Аутентификация**: djangorestframework-simplejwt (JWT).
- **Документация API**: drf-spectacular (OpenAPI + Swagger UI).
- **Фоновые задачи**: Celery, Redis, django-celery-beat.
- **Интеграция с Telegram**: Telegram Bot API (через requests).

---

## Установка и запуск (локально)

### 1. Клонирование и зависимости

```bash
git clone <repo_url>
cd SkyPro_course_project_5
poetry install
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `.env.template`:

```env
SECRET_KEY=your_secret_key
DEBUG=True

NAME=habit_db
USER=habit_user
PASSWORD=habit_password
HOST=localhost
PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### 3. Миграции и суперпользователь

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Запуск Redis

Если Redis установлен локально:

```bash
sudo service redis-server start
redis-cli ping  # должен вернуть PONG
```

### 5. Запуск приложения и Celery

В разных терминалах:

```bash
# Django
python manage.py runserver
```

```bash
# Celery worker
celery -A config.celery worker -l info
```

```bash
# Celery beat с django-celery-beat
celery -A config.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## Основные эндпоинты

Базовый префикс: `/api/`

### Авторизация

- `POST /api/auth/register/` – регистрация пользователя (username, email, password, password2).
- `POST /api/auth/token/` – получение JWT-токена (access/refresh).
- `POST /api/auth/token/refresh/` – обновление access-токена.

### Привычки

- `GET /api/habits/` – список привычек текущего пользователя (с пагинацией).
- `POST /api/habits/` – создание привычки.
- `GET /api/habits/{id}/` – просмотр привычки.
- `PUT/PATCH /api/habits/{id}/` – редактирование своей привычки.
- `DELETE /api/habits/{id}/` – удаление своей привычки.
- `GET /api/habits/public/` – список публичных привычек (без авторизации, только чтение).

---

## Модель Habit (основные поля)

- `user` – владелец привычки.
- `place` – место выполнения.
- `time` – время выполнения.
- `action` – действие (описание привычки).
- `is_pleasant` – признак «приятной» привычки.
- `related_habit` – связанная приятная привычка (в качестве вознаграждения).
- `periodicity` – периодичность в днях (1–7, по умолчанию 1).
- `reward` – текстовое вознаграждение.
- `time_to_execute` – время выполнения в секундах (≤ 120).
- `is_public` – признак публичности.

Валидаторы не позволяют:

- одновременно указывать `reward` и `related_habit`;
- задавать связанную привычку, если она не `is_pleasant=True`;
- у приятной привычки иметь `reward` или `related_habit`;
- выставлять `periodicity` меньше 1 или больше 7.

---

## Telegram-уведомления

- Используется ботовый токен `TELEGRAM_BOT_TOKEN` и `CHAT_ID` из `.env`.
- Celery-задача собирает актуальные привычки и отправляет напоминания в Telegram.
- Периодичность рассылки настраивается через django-celery-beat (модель `PeriodicTask`) в админке.

---

## Тесты и покрытие

- Тесты написаны на стандартном `unittest` (`django.test.TestCase`).
- Покрываются:
  - модель `Habit` и её валидаторы;
  - API привычек (CRUD, публичные привычки);
  - регистрация и авторизация (JWT);
  - задача отправки напоминаний в Telegram (с моками requests).
- Покрытие по `coverage` ≈ **94%** (выше требуемых 80%).

---

## Документация API

- OpenAPI-схема: `GET /api/schema/`
- Swagger UI: `GET /api/docs/`

Используется `drf-spectacular`, схема генерируется автоматически на основе DRF-вью и сериализаторов.

---