# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'text',
        'task',
        'user',
        'created_at',
    ]
    list_display_links = (
        'id',
        'text',
    )
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ('id', 'task', 'user')
    list_filter = ('task', 'user')
