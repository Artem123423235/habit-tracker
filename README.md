# Habit Tracker

[![CI](https://github.com/Artem123423235/habit-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Artem123423235/habit-tracker/actions/workflows/ci.yml)

Django-приложение для трекинга привычек с Telegram-ботом, платными курсами и интеграцией платежей.

## Стек

- **Backend:** Django 5 + DRF
- **DB:** PostgreSQL 16
- **Cache/Broker:** Redis 7
- **Async:** Celery + Celery Beat
- **Bot:** python-telegram-bot
- **Infra:** Docker + Docker Compose
- **CI:** GitHub Actions

## Возможности

- Регистрация / авторизация по JWT
- CRUD привычек с валидацией (периодичность, длительность, связанные привычки)
- Публичные и приватные привычки
- Отправка напоминаний в Telegram через Celery-задачи
- Платные курсы и подписки
- Интеграция с платёжной системой (Stripe)
- Telegram-бот для управления привычками
- Пагинация, сортировка, права доступа
- Покрытие тестами (Django TestCase)

## Быстрый старт

```bash
git clone https://github.com/Artem123423235/habit-tracker.git
cd habit-tracker
cp .env.example .env       # заполнить SECRET_KEY и TELEGRAM_BOT_TOKEN
docker compose up -d
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser

docker compose run --rm web python manage.py test

├── bot/                # Telegram-бот
├── config/             # Django settings, urls, celery, wsgi
├── courses/            # Курсы и подписки
├── habits/             # Привычки + API + валидация
├── payments/           # Платежи (Stripe)
├── users/              # Пользователи, Telegram-профили
├── .github/workflows/  # CI
├── docker-compose.yml
└── Dockerfile


## 🚀 Деплой

Приложение задеплоено на VPS и доступно по адресу:

- **Прод:** http://<ТВОЙ_IP>/  (Django + админка)
- **Админка:** http://<ТВОЙ_IP>/admin/

### Автодеплой (GitHub Actions)

Каждый `git push` в ветку `main` автоматически:
1. Заходит по SSH на сервер
2. Подтягивает свежий код из GitHub
3. Пересобирает Docker-образы
4. Запускает миграции Django

Workflow: `.github/workflows/deploy.yml`

### Инфраструктура

| Сервис | Контейнер | Порт наружу |
|---|---|---|
| Nginx (reverse proxy) | systemd | **0.0.0.0:80** |
| Django (gunicorn, 3 воркера) | habit_web | 127.0.0.1:8000 |
| PostgreSQL 15 | habit_db | **закрыт** |
| Redis 7 | habit_redis | **закрыт** |
| Celery worker (напоминания) | habit_celery | — |
| Celery beat (планировщик) | habit_celery_beat | — |
| Telegram-бот (aiogram) | habit_bot | — |

**Статика** отдаётся Nginx напрямую из `staticfiles/`.  
**Безопасность:** БД и Redis не проброшены наружу — только внутри docker-сети. Django доступен только через Nginx.

### Ручной деплой (если понадобится)

```bash
ssh deploy@45.90.33.53
cd ~/habit-tracker
git fetch origin && git reset --hard origin/main
docker compose up -d --build
docker compose exec web python manage.py migrate --noinput

