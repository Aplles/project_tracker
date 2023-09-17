# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Timer


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'result_time',
        'task_user',
        'start_time',
        'end_time',
    ]
    list_display_links = (
        'id',
        'result_time',
    )
    readonly_fields = ['id', 'result_time', 'start_time', 'end_time']
    ordering = ('id', 'task_user')
    list_filter = ('task_user', )
