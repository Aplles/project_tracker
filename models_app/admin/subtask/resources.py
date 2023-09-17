# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Subtask


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'is_done',
        'task',
    ]
    list_display_links = (
        'id',
        'title',
    )
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ('id', 'is_done', 'task')
    list_filter = ('is_done', 'task')
