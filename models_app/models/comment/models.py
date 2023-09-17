# -*- coding: utf8 -*-
from django.db import models


class Comment(models.Model):
    """ Модель комментария """

    text = models.CharField(max_length=255, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        verbose_name='Задача',
        related_name='comments_task'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='comments_user'
    )

    def __str__(self):
        return f''

    class Meta:
        db_table = 'comments'
        app_label = 'models_app'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
