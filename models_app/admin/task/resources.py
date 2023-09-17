# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import (
    Task,
    Subtask,
    Document,
    Comment
)


class SubTaskInline(admin.TabularInline):
    model = Subtask
    extra = 0


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Общая информация',
            {
                'fields': [
                    'id',
                    'title',
                    'description',
                    'time_per_task',
                    'status',
                    'project',
                ]
            }
        ),
        (
            'Прочая информация',
            {
                'fields':
                    [
                        'created_at',
                        'updated_at'
                    ]
            }
        ),
    ]
    list_display = [
        'id',
        'title',
        'time_per_task',
        'status',
        'project',
    ]
    list_display_links = (
        'id',
        'title',
    )
    inlines = (SubTaskInline, DocumentInline, CommentInline)
    ordering = ('id', 'time_per_task', 'status', 'project')
    list_filter = ('time_per_task', 'status', 'project')
    readonly_fields = ['id', 'created_at', 'updated_at']
    save_on_top = True
