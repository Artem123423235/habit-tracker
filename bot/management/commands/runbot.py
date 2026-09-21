# bot/management/commands/runbot.py
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Запускает Telegram-бота в режиме long-polling"

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        if not token:
            raise CommandError("TELEGRAM_BOT_TOKEN не задан в переменных окружения")

        asyncio.run(self._run(token))

    async def _run(self, token: str):
        bot = Bot(token=token)
        dp = Dispatcher()

        @dp.message(CommandStart())
        async def start(message: Message):
            await message.answer(
                f"Привет, {message.from_user.first_name}! "
                "Я бот трекера привычек."
            )

        @dp.message(F.text)
        async def echo(message: Message):
            await message.answer(f"Эхо: {message.text}")

        self.stdout.write(self.style.SUCCESS("Бот запущен (aiogram 3), polling..."))
        await dp.start_polling(bot)
