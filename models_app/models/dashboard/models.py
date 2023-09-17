# -*- coding: utf8 -*-
from django.db import models


class Dashboard(models.Model):
    """ Модель мониторинга """
    status = models.CharField(max_length=255, verbose_name='Статус (Название колонки)')

    def __str__(self):
        return f'Статус: {self.status}'

    class Meta:
        db_table = 'dashboards'
        app_label = 'models_app'
        verbose_name = 'Мониторинг'
        verbose_name_plural = 'Мониторинги'
