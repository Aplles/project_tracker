from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Project

from models_app.models import Dashboard


class DashboardDeleteService(ServiceWithResult):
    id = forms.IntegerField()
    project_id = forms.IntegerField()

    custom_validations = ['_dashboard_presence', '_project_presence']

    def process(self):
        self.run_custom_validations()
        self._delete()
        return self

    def _delete(self):
        current_position = self._dashboard.position
        dashboards = Dashboard.objects.filter(
            position__gte=current_position,
            project=self._project
        )

        update_dashboards = []
        for dashboard in dashboards:
            dashboard.position = current_position
            current_position += 1
            update_dashboards.append(dashboard)
        Dashboard.objects.bulk_update(update_dashboards, ['position'])

        self._dashboard.delete()

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
