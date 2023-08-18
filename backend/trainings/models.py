from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TrainingType(models.Model):
    """Training type model."""

    name = models.CharField(
        verbose_name='Тип тренировки', max_length=200, blank=False, unique=True
    )

    class Meta:
        verbose_name = "Тип тренировки"
        verbose_name_plural = "Типы тренировки"
        ordering = ['name']

    def __str__(self):
        return self.name[:30]


class Training(models.Model):
    """Training model."""

    author = models.ForeignKey(
        User, verbose_name='Автор тренировки', on_delete=models.CASCADE,
        related_name='trainings'
    )
    type = models.ForeignKey(
        TrainingType, verbose_name='Тип тренировки', on_delete=models.SET_NULL,
        related_name='trainings', blank=True, null=True
    )
    started_at = models.DateTimeField(
        verbose_name='Время начала', default=datetime.now,
        blank=False, db_index=True
    )
    finished_at = models.DateTimeField(
        verbose_name='Время окончания', default=datetime.now, db_index=True
    )
    distance = models.FloatField(
        verbose_name='Дистанция', default=0
    )
    steps_num = models.IntegerField(
        verbose_name='Количество шагов', default=0
    )
    completed = models.BooleanField(
        verbose_name='Завершение тренировки', default=False
    )
    reminder = models.BooleanField(
        verbose_name='Напоминание о тренировке', default=False
    )
    raiting = models.SmallIntegerField(
        verbose_name='Рейтинг', blank=True, null=True
    )

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ['started_at']

    def __str__(self):
        return f'{self.author} {self.type}'
