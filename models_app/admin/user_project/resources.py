# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import UserProject


@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'project',
    ]
    list_display_links = (
        'id',
    )
    ordering = ('id', 'user', 'project')
    list_filter = ('user', 'project')