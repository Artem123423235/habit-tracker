# habits/tasks.py
import logging
from datetime import timedelta

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Habit

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id: str, text: str) -> bool:
    """Отправить сообщение в Telegram. Возвращает True при успехе."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN не задан — сообщение не отправлено")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.error("Ошибка отправки в Telegram (chat_id=%s): %s", chat_id, exc)
        return False


@shared_task
def send_habit_reminders():
    """
    Ищет привычки, у которых время наступает в ближайшие 5 минут,
    и отправляет пользователю напоминание в Telegram.
    """
    now = timezone.localtime()
    window_end = (now + timedelta(minutes=5)).time()

    habits = (
        Habit.objects
        .filter(
            user__telegram_profile__isnull=False,
            user__telegram_profile__chat_id__isnull=False,
            time__gte=now.time(),
            time__lte=window_end,
        )
        .select_related("user", "user__telegram_profile")
    )

    sent = 0
    for habit in habits:
        chat_id = habit.user.telegram_profile.chat_id
        text = (
            f"⏰ Напоминание: {habit.action}\n"
            f"📍 Место: {habit.place}\n"
            f"🕐 Время: {habit.time.strftime('%H:%M')}"
        )
        if send_telegram_message(chat_id, text):
            sent += 1

    return f"Отправлено напоминаний: {sent}"
