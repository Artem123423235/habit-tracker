from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Связанная привычка'
    )
    frequency = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Периодичность (дней)'
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveSmallIntegerField(
        default=120,
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name='Длительность (секунды)'
    )
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action

    class Meta:
        ordering = ["-id"]
