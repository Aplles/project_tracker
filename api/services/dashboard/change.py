from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Project

from models_app.models import Dashboard


class DashboardChangeService(ServiceWithResult):
    DIRECTION_CHOICES = (
        ("left", "left"),
        ("right", "right")
    )
    id = forms.IntegerField()
    project_id = forms.IntegerField()
    direction = forms.ChoiceField(choices=DIRECTION_CHOICES)

    custom_validations = ['_dashboard_presence', '_project_presence']

    def process(self):
        self.run_custom_validations()
        self._change()
        return self

    def _change(self):
        buf = self._dashboard.position
        if self.cleaned_data['direction'] == 'left':
            direction_dashboard = Dashboard.objects.get(position=buf - 1, project=self._project)
        else:
            direction_dashboard = Dashboard.objects.get(position=buf + 1, project=self._project)

        self._dashboard.position = direction_dashboard.position
        direction_dashboard.position = buf
        self._dashboard.save()
        direction_dashboard.save()

    @property
    @lru_cache
    def _dashboard(self):
        try:
            return Dashboard.objects.get(id=self.cleaned_data['id'])
        except Dashboard.DoesNotExist:
            return None

    @property
    @lru_cache
    def _project(self):
        try:
            return Project.objects.get(id=self.cleaned_data['project_id'])
        except Project.DoesNotExist:
            return None

    def _dashboard_presence(self):
        if not self._dashboard:
            raise NotFound("Dashboard with this id not found")

    def _project_presence(self):
        if not self._project:
            raise NotFound("Project with this id not found")
