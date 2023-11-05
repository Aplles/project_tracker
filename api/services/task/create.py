from functools import lru_cache

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult, ServiceOutcome
from rest_framework.exceptions import NotFound, ValidationError
from django import forms

from api.services.subtask.create import SubTaskCreateService
from models_app.models import Project, Task, Dashboard, User


class TaskCreateService(ServiceWithResult):
    id = forms.IntegerField()
    title_task = forms.CharField()
    desc_task_create = forms.CharField()
    time_per_task = forms.CharField()
    status_task = forms.CharField()
    user = ModelField(User)

    custom_validations = ['check_project', 'check_status', 'count_subtask']

    def process(self):
        self.run_custom_validations()
        self.result = self._create
        return self

    @property
    def _create(self) -> Task:
        task = Task.objects.create(
            title=self.cleaned_data['title_task'],
            description=self.cleaned_data['desc_task_create'],
            time_per_task=self.cleaned_data['time_per_task'],
            status=self._status,
            project=self._project,
            author=self.cleaned_data['user'],
        )
        self._create_subtasks(task)
        return task

    def _create_subtasks(self, task: Task) -> None:
        for index in range(0, int(self.data['count_subtask'])):
            ServiceOutcome(SubTaskCreateService, {
                'title': self.data[f'subtask_{index}_title'],
                'description': self.data[f'subtask_{index}_description'],
                'task': task
            })

    @property
    @lru_cache
    def _status(self):
        try:
            return Dashboard.objects.get(id=self.cleaned_data['status_task'])
        except Project.DoesNotExist:
            return None

    @property
    @lru_cache
    def _project(self):
        try:
            return Project.objects.get(id=self.cleaned_data['id'])
        except Project.DoesNotExist:
            return None

    def check_project(self):
        if not self._project:
            raise NotFound("Project with this id is not found")

    def check_status(self):
        if not self._status:
            raise NotFound("Dashboard with this id is not found")

    def count_subtask(self):
        try:
            int(self.data['count_subtask'])
        except ValueError:
            raise ValidationError('count_subtask must be int')
