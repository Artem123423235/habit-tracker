from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class SmokeTests(TestCase):
    """Минимальные тесты: Django поднимается, БД доступна, сервер отвечает."""

    def test_database_is_reachable(self):
        count = User.objects.count()
        self.assertGreaterEqual(count, 0)

    def test_server_responds_without_500(self):
        response = self.client.get("/")
        self.assertLess(response.status_code, 500)