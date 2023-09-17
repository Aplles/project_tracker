# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Dashboard


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
    ]
    list_display_links = (
        'id',
    )
    ordering = ('id', 'status',)
