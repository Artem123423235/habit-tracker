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


