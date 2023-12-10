# -*- coding: utf8 -*-
from django.db import models


class Task(models.Model):
    """ Модель задачи """

    title = models.CharField(max_length=255, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    time_per_task = models.IntegerField(verbose_name="Часов на задачу")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.ForeignKey(
        'Dashboard',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_status',
        verbose_name='Статус задачи'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='tasks_project',
        verbose_name='Проект'
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='tasks_author',
        verbose_name='Менеджер задачи'
    )

    def members(self):
        return self.tasks_task.all()

    def __str__(self):
        return f'{self.project} - {self.title}'

    class Meta:
        db_table = 'tasks'
        app_label = 'models_app'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
