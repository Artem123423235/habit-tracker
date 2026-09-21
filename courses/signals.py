from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail

from .models import Lesson, Course, Subscription


@receiver(post_save, sender=Lesson)
def notify_subscribers_about_lesson_update(sender, instance, **kwargs):
    course = instance.course
    now = timezone.now()

    # Если курс ещё ни разу не уведомлялся, или с последнего уведомления прошло >= 4 часов
    if course.last_notified_at is None or (now - course.last_notified_at) >= timedelta(hours=4):
        # Находим подписчиков
        subscriptions = Subscription.objects.filter(course=course)
        emails = [sub.user.email for sub in subscriptions if sub.user.email]

        if emails:
            send_mail(
                subject=f'Курс "{course.title}" обновлён',
                message=f'В курсе появились новые материалы. Проверьте обновления!',
                from_email=None,  # использует DEFAULT_FROM_EMAIL
                recipient_list=emails,
            )

        course.last_notified_at = now
        course.save(update_fields=['last_notified_at'])
