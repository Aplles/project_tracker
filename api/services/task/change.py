from functools import lru_cache

from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Dashboard, Task, Project


class TaskChangeService(ServiceWithResult):
    status_id = forms.CharField(required=False)
    task_id = forms.CharField()
    id = forms.IntegerField()

    custom_validations = [
        'dashboard_presence',
        'task_presence',
        'project_presence'
    ]

    def process(self):
        self.run_custom_validations()
        self._change()
        return self

    def _change(self):
        if self.cleaned_data.get('status_id'):
            self._task.status = self._dashboard
        self._task.save()

    @property
    @lru_cache
    def _dashboard(self):
        try:
            return Dashboard.objects.get(id=self.cleaned_data['status_id'])
        except Dashboard.DoesNotExist:
            return None

    @property
    @lru_cache
    def _task(self):
        try:
            return Task.objects.get(id=self.cleaned_data['task_id'])
        except Task.DoesNotExist:
            return None

    @property
    @lru_cache
    def _project(self):
        try:
            return Project.objects.get(id=self.cleaned_data['id'])
        except Project.DoesNotExist:
            return None

    def dashboard_presence(self):
        if not self._dashboard and self.cleaned_data.get('status_id'):
            raise NotFound("Dashboard with this id is not found")

    def task_presence(self):
        if not self._task:
            raise NotFound("Task with this id is not found")

    def project_presence(self):
        if not self._project:
            raise NotFound("Project with this id is not found")
