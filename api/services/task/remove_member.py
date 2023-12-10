from functools import lru_cache

from django import forms
from rest_framework.exceptions import PermissionDenied, NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, UserProject, Task, TaskUser


class TaskMemberDeleteService(ServiceWithResult):
    member_id = forms.IntegerField()
    project_id = forms.IntegerField()
    id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['task_presence', 'check_right', 'member_presence',  'task_user_presence']

    def process(self):
        self.run_custom_validations()
        self._remove()
        return self

    def _remove(self):
        self._task_user.delete()

    @property
    @lru_cache
    def _member(self):
        try:
            return User.objects.get(id=self.cleaned_data['member_id'])
        except User.DoesNotExist:
            return None

    @property
    @lru_cache
    def _task_user(self):
        try:
            return TaskUser.objects.get(
                user=self._member,
                task=self._task
            )
        except TaskUser.DoesNotExist:
            return None

    @property
    @lru_cache
    def _task(self):
        try:
            return Task.objects.get(id=self.cleaned_data['id'])
        except Task.DoesNotExist:
            return None

    def task_presence(self):
        if not self._task:
            raise NotFound("Task with this id not found")

    def task_user_presence(self):
        if not self._task_user:
            raise NotFound("Task user with this id not found")

    def member_presence(self):
        if not self._member:
            raise NotFound("User(member) with this id not found")

    def check_right(self):
        if not UserProject.objects.filter(
                user=self.cleaned_data['user'],
                project_id=self.cleaned_data['project_id']
        ) or self.cleaned_data['user'].role != User.manager:
            raise PermissionDenied("PermissionDenied")
