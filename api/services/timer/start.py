from django.utils import timezone
from functools import lru_cache

from rest_framework.exceptions import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import (
    User,
    Timer,
    TaskUser,
    Comment,
    Task
)


class TimerStartService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['task_presence', 'task_user_presence', ]

    def process(self):
        self.run_custom_validations()
        self._start()
        self.result = self._comment
        return self

    def _start(self):
        Timer.objects.create(
            start_time=timezone.now(),
            task_user=self._task_user
        )

    @property
    def _comment(self):
        return Comment.objects.create(
            text=f"{self._user.last_name} {self._user.first_name} приступил к выполнению задачи",
            task=self._task,
            user=self._user
        )

    @property
    @lru_cache
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    @lru_cache
    def _task(self):
        try:
            return Task.objects.get(id=self.cleaned_data['id'])
        except Task.DoesNotExist:
            return None

    @property
    @lru_cache
    def _task_user(self):
        try:
            return TaskUser.objects.get(
                user=self._user,
                task=self._task
            )
        except TaskUser.DoesNotExist:
            return None

    def task_user_presence(self):
        if not self._task_user:
            raise NotFound("Task user with this id not found")

    def task_presence(self):
        if not self._task:
            raise NotFound("Task with this id not found")
