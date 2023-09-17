# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]
    list_display_links = (
        'id',
    )
    inlines = (TaskInline,)
    ordering = ('id', 'name',)
