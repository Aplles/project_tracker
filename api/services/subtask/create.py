from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Task, Subtask


class SubTaskCreateService(ServiceWithResult):
    title = forms.CharField()
    description = forms.CharField()
    is_done = forms.CharField(required=False)

    custom_validations = ["task_presence", ]

    def process(self):
        self.run_custom_validations()
        self.result = self._create
        return self

    @property
    def _create(self):
        return Subtask.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            is_done=self.cleaned_data['is_done'] or False,
            task=self._task,
        )

    @property
    def _task(self):
        if isinstance(self.data['task'], Task):
            return self.data['task']
        try:
            return Task.objects.get(id=self.data['task'])
        except Task.DoesNotExist:
            return None

    def task_presence(self):
        if not self._task:
            raise NotFound("Task with this id is not found")