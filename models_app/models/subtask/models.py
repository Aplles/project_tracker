# -*- coding: utf8 -*-
from django.db import models


class Subtask(models.Model):
    """ Модель подзадачи """

    title = models.CharField(max_length=255, verbose_name='Название подзадачи')
    description = models.TextField(verbose_name='Описание подзадачи')
    is_done = models.BooleanField(default=False, verbose_name='Выполнена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks_task',
        verbose_name='Задача'
    )

    def __str__(self):
        return f'{self.title} - {self.is_done} - {self.task}'

    class Meta:
        db_table = 'subtasks'
        app_label = 'models_app'
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'
