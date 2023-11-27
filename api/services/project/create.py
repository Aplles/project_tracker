from functools import lru_cache

from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Project
from models_app.models import UserProject

from models_app.models import User


class ProjectCreateService(ServiceWithResult):
    name = forms.CharField()
    image = forms.ImageField()
    user = ModelField(User)

    def process(self):
        self.result = self._project
        self._append_user_project()
        return self

    @property
    @lru_cache
    def _project(self):
        return Project.objects.create(
            name=self.cleaned_data['name'],
            image=self.cleaned_data['image'],
        )

    def _append_user_project(self):
        UserProject.objects.create(
            user=self.cleaned_data['user'],
            project=self._project
        )
