# -*- coding: utf8 -*-
from django.contrib import admin
from models_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Общая информация',
            {
                'fields': [
                    'email',
                    'username',
                    'password',
                    'avatar',
                    'role',
                ]
            }
        ),
        (
            'Права доступа',
            {
                'fields':
                    [
                        'is_superuser',
                        'user_permissions',
                        'groups',
                        'is_staff',
                        'is_active'
                    ]
            }
        ),
        (
            'Прочая информация',
            {
                'fields':
                    [
                        'last_login',
                        'date_joined',
                        'first_name',
                        'last_name',
                        'created_at',
                        'updated_at'
                    ]
            }
        ),
    ]
    save_on_top = True
    list_filter = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_display = [
        'id',
        'email',
        'username',
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display_links = (
        'id',
        'email',
        'username',
    )
    ordering = ('id', 'email', 'username', 'created_at', 'updated_at')
