from functools import lru_cache

from django import forms
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from service_objects.services import ServiceWithResult

from models_app.models import User


class UserAuthService(ServiceWithResult):
    login = forms.CharField()
    password_1 = forms.CharField()
    password_2 = forms.CharField(required=False)

    custom_validations = [
        'user_presence',
        'check_len',
        'check_password',
    ]

    def process(self):
        if not self.cleaned_data.get("password_2"):
            if not self.authenticate:
                self.add_error('user', 'Неверный логин или пароль')
            self.result = self.authenticate
        else:
            self.run_custom_validations()
            self.result = self._register()
        return self

    @property
    @lru_cache
    def authenticate(self):
        return authenticate(
            self.data['request'],
            email=self.cleaned_data.get('login'),
            password=self.cleaned_data.get('password_1')
        )

    def _register(self):
        if not self.errors:
            user = User.objects.create_user(
                email=self.cleaned_data.get('login'),
                username=self.cleaned_data.get('login'),
                password=self.cleaned_data.get('password_1'),
                first_name="Максим",
                last_name="Караичев",
            )
            Token.objects.create(user=user)
            return user
        return self.errors

    def user_presence(self):
        if self.authenticate:
            self.add_error("user", "Такой пользователь уже есть")

    def check_len(self):
        if not (self.cleaned_data.get('password_1') and self.cleaned_data.get('password_2')):
            self.add_error("password", "Должны быть введены оба пароля")

    def check_password(self):
        if self.cleaned_data.get('password_1') != self.cleaned_data.get('password_2'):
            self.add_error("password", "Введенные пароли не совпадают")