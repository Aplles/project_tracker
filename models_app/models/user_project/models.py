# -*- coding: utf8 -*-
from django.db import models


class UserProject(models.Model):
    """ Модель проектов пользователя """

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='user_projects',
        verbose_name='Пользователь'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='users_project',
        verbose_name='Проект'
    )

    def count_tasks(self):
        return self.user.tasks_user.filter(task__project=self.project).count()

    def __str__(self):
        return f'Проект: {self.project}, Пользователь: {self.user}'

    class Meta:
        db_table = 'user_project'
        app_label = 'models_app'
        verbose_name = 'Проекты пользователя'
        verbose_name_plural = 'Проекты пользователей'
