from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создание тестовых платежей'

    def handle(self, *args, **options):
        users = list(User.objects.all())
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not users:
            self.stdout.write(self.style.WARNING('Сначала создайте пользователей'))
            return
        if not course or not lesson:
            self.stdout.write(self.style.WARNING('Сначала создайте хотя бы один курс и один урок'))
            return

        payments = [
            {'user': users[0], 'course': course, 'amount': 1000, 'method': 'cash'},
            {'user': users[0], 'lesson': lesson, 'amount': 500, 'method': 'transfer'},
            {'user': users[1] if len(users) > 1 else users[0], 'course': course,
             'amount': 2000, 'method': 'transfer'},
        ]

        for data in payments:
            Payment.objects.create(
                user=data['user'],
                course=data.get('course'),
                lesson=data.get('lesson'),
                amount=data['amount'],
                payment_method=data['method'],
            )

        self.stdout.write(self.style.SUCCESS('Тестовые платежи успешно созданы'))
