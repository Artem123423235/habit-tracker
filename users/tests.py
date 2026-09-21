"""
Тесты аутентификации и регистрации.

Используем встроенный django.test.TestCase — никаких pytest/conftest не нужно.
Все эндпоинты — из djoser (подключены в config/urls.py как /auth/...).
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserAuthAPITests(TestCase):
    """Проверяет работоспособность регистрации, логина и защиты эндпоинтов."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/auth/users/"
        self.jwt_create_url = "/auth/jwt/create/"
        self.me_url = "/auth/users/me/"
        self.email = "testuser@example.com"
        self.password = "StrongPass!2024"

    def test_admin_page_responds(self):
        """
        Django и БД живы: /admin/ доступен.
        Аноним получает 302 (редирект на /admin/login/),
        залогиненный — 200.
        """
        response = self.client.get("/admin/")
        self.assertIn(
            response.status_code, (200, 302),
            msg=f"/admin/ вернул {response.status_code}",
        )

    def test_register_user_via_djoser(self):
        """POST /auth/users/ создаёт пользователя в БД и возвращает 201."""
        payload = {
            "email": self.email,
            "password": self.password,
            "re_password": self.password,  # на случай USER_CREATE_PASSWORD_RETYPE=True
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            msg=f"Регистрация упала: {response.status_code} {response.content!r}",
        )
        self.assertTrue(
            User.objects.filter(email=self.email).exists(),
            msg=f"Пользователь {self.email} не создан в БД",
        )

    def test_login_returns_jwt(self):
        """POST /auth/jwt/create/ с валидными email+password даёт access+refresh."""
        User.objects.create_user(email=self.email, password=self.password)

        response = self.client.post(
            self.jwt_create_url,
            {"email": self.email, "password": self.password},
            format="json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg=f"Логин упал: {response.status_code} {response.content!r}",
        )
        self.assertIn("access", response.data, msg="Нет поля 'access' в ответе")
        self.assertIn("refresh", response.data, msg="Нет поля 'refresh' в ответе")

    def test_login_with_wrong_password_fails(self):
        """Неверный пароль → 401."""
        User.objects.create_user(email=self.email, password=self.password)

        response = self.client.post(
            self.jwt_create_url,
            {"email": self.email, "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_auth(self):
        """GET /auth/users/me/ без JWT → 401."""
        response = self.client.get(self.me_url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED,
            msg=f"Ожидали 401, получили {response.status_code}",
        )
