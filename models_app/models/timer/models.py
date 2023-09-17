# -*- coding: utf8 -*-
from django.db import models


class Timer(models.Model):
    """ Модель таймера """

    start_time = models.DateTimeField(
        verbose_name="Время начала",
        null=True,
        blank=True
    )
    end_time = models.DateTimeField(
        verbose_name="Время конца",
        null=True,
        blank=True
    )
    result_time = models.DateTimeField(
        verbose_name="Время затраченное на задачу",
        null=True,
        blank=True
    )
    task_user = models.ForeignKey(
        'TaskUser',
        on_delete=models.CASCADE,
        related_name='timers_task_user',
        verbose_name='Задачи пользователя'
    )

    def __str__(self):
        return f'Время начала: {self.start_time}. Время конца: {self.end_time}'

    class Meta:
        db_table = 'timers'
        app_label = 'models_app'
        verbose_name = 'Таймер'
        verbose_name_plural = 'Таймеры'
