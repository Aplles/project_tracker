from functools import lru_cache

from django import forms
from rest_framework.exceptions import PermissionDenied, NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, UserProject, Task


class TaskDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)
    project_id = forms.IntegerField()

    custom_validations = ['task_presence', 'check_right']

    def process(self):
        self.run_custom_validations()
        self._delete()
        return self

    def _delete(self):
        self._task.delete()

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

    def check_right(self):
        if not UserProject.objects.filter(
                user=self.cleaned_data['user'],
                project_id=self.cleaned_data['project_id']
        ) or self.cleaned_data['user'].role != User.manager:
            raise PermissionDenied("PermissionDenied")
