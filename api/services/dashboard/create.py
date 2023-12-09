from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Project

from models_app.models import Dashboard


class DashboardCreateService(ServiceWithResult):
    id = forms.IntegerField()
    status = forms.CharField()
    color = forms.CharField()

    def process(self):
        self.run_custom_validations()
        self._create()
        return self

    def _create(self):
        return Dashboard.objects.create(
            status=self.cleaned_data['status'],
            project=self._project,
            color=self.cleaned_data['color'],
            position=self._position
        )

    @property
    @lru_cache
    def _project(self):
        try:
            return Project.objects.get(id=self.cleaned_data['id'])
        except Project.DoesNotExist:
            return None

    @property
    def _position(self):
        dashboards = Dashboard.objects.filter(project=self._project)
        if dashboards:
            return dashboards.last().position
        return 0

    def check_project(self):
        if not self._project:
            raise NotFound("Project with this id is not found")
