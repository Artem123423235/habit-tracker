"""
Тесты Habit API и публичных эндпоинтов.

Проверяют:
- защиту /api/habits/ через JWT;
- работу OpenAPI-схемы (drf-spectacular).
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class HabitAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.habits_url = "/api/habits/"
        self.schema_url = "/api/schema/"

        self.user = User.objects.create_user(
            email="habituser@example.com",
            password="StrongPass!2024",
        )

    def _authenticate(self):
        """Подкладывает валидный JWT-токен в заголовки клиента."""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def test_habits_requires_auth(self):
        """/api/habits/ без токена → 401."""
        response = self.client.get(self.habits_url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"Ожидали 401, получили {response.status_code}",
        )

    def test_habits_list_with_token(self):
        """/api/habits/ с валидным JWT → 200 (свои привычки)."""
        self._authenticate()
        response = self.client.get(self.habits_url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f"Ожидали 200, получили {response.status_code}: {response.content!r}",
        )

    def test_openapi_schema_available(self):
        """/api/schema/ отдаёт 200 — drf-spectacular настроен корректно."""
        response = self.client.get(self.schema_url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f"Схема недоступна: {response.status_code}",
        )
