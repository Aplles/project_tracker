from functools import lru_cache

from django import forms
from rest_framework.exceptions import NotFound, ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, UserProject, Project


class InviteService(ServiceWithResult):
    user = ModelField(User)
    id = forms.UUIDField()

    custom_validations = ['project_presence', 'user_project_presence']

    def process(self):
        self.run_custom_validations()
        self._invite()
        self.result = self._project
        return self

    def _invite(self):
        UserProject.objects.create(
            user=self.cleaned_data['user'],
            project=self._project
        )

    @property
    @lru_cache
    def _project(self):
        try:
            return Project.objects.get(uuid=self.cleaned_data['id'])
        except Project.DoesNotExist:
            return None

    def project_presence(self):
        if not self._project:
            raise NotFound("Project with this uuid not found")

    def user_project_presence(self):
        if UserProject.objects.filter(
                user=self.cleaned_data['user'],
                project=self._project
        ):
            raise ValidationError("User already in project")
