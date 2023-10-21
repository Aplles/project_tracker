# -*- coding: utf8 -*-
from django.db import models


class Dashboard(models.Model):
    """ Модель мониторинга """
    status = models.CharField(max_length=255, verbose_name='Статус (Название колонки)')
    position = models.PositiveIntegerField(default=0, verbose_name="Позиция")
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='dashboards_project',
        verbose_name='Проект'
    )
    color = models.CharField(max_length=7, default="#FF0000", verbose_name="Цвет")

    def __str__(self):
        return f'Статус: {self.status}. Позиция: {self.position}'

    class Meta:
        db_table = 'dashboards'
        app_label = 'models_app'
        verbose_name = 'Мониторинг'
        verbose_name_plural = 'Мониторинги'
