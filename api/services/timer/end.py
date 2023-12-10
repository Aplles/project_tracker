from django.utils import timezone
from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import (
    User,
    Task,
    TaskUser,
    Timer,
    Comment
)


class TimerEndService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['task_presence', 'task_user_presence', 'timer_presence']

    def process(self):
        self.run_custom_validations()
        self._end()
        self.result = self._comment
        return self

    @property
    def _comment(self):
        return Comment.objects.create(
            text=f"{self._user.last_name} {self._user.first_name} закончил выполнение задачи.\n"
                 f"Затраченное время: {self.format_duration(self._timer.result_time)}.\n"
                 f"Время окончания: ",
            task=self._task,
            user=self._user
        )

    @staticmethod
    def format_duration(duration):
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} часов {minutes} минут {seconds} секунд"

    def _end(self):
        self._timer.end_time = timezone.now()
        self._timer.result_time = self._timer.end_time - self._timer.start_time
        self._timer.save()

    @property
    @lru_cache
    def _timer(self):
        try:
            return Timer.objects.get(task_user=self._task_user, result_time__isnull=True)
        except Timer.DoesNotExist:
            return None

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

    def timer_presence(self):
        if not self._timer:
            raise NotFound("Timer with this task user not found")
