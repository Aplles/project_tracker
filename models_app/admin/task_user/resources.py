# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import TaskUser


@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'task',
    ]
    list_display_links = (
        'id',
    )
    ordering = ('id', 'user', 'task')
    list_filter = ('user', 'task')
