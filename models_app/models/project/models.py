# -*- coding: utf8 -*-
from django.db import models


class Project(models.Model):
    """ Модель проекта """

    name = models.CharField(max_length=255, verbose_name="Название проекта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        db_table = 'projects'
        app_label = 'models_app'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
