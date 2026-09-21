from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    """
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__isnull=False,
        last_login__lt=month_ago
    )

    count = inactive_users.update(is_active=False)
    print(f'Blocked {count} inactive users')
    return count
