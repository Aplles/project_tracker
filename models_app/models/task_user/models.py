# -*- coding: utf8 -*-
from django.db import models


class TaskUser(models.Model):
    """ Модель задач пользователя """

    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_user',
        verbose_name='Пользователь'
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='tasks_task',
        verbose_name='Задача'
    )

    def __str__(self):
        return f'{self.user} - {self.task}'

    class Meta:
        db_table = 'tasks_user'
        app_label = 'models_app'
        verbose_name = 'Задача пользователя'
        verbose_name_plural = 'Задачи пользователя'
