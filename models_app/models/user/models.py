# -*- coding: utf8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя """

    manager = 'manager'
    programmer = 'programmer'

    TYPE = [
        (manager, 'Менеджер'),
        (programmer, 'Программист'),
    ]
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Фото профиля')
    role = models.CharField(max_length=50, choices=TYPE, default=programmer)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} {self.username}'

    class Meta:
        db_table = 'users'
        app_label = 'models_app'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
