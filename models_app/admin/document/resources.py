# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'file',
        'position',
        'task',
    ]
    list_display_links = (
        'id',
        'name',
    )
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ('id', 'position', 'task')
    list_filter = ('position', 'task')
