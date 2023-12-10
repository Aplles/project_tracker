from functools import lru_cache

from rest_framework.exceptions import NotFound, PermissionDenied
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import UserProject, User


class UserRemoveService(ServiceWithResult):
    id = forms.IntegerField()
    user_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ["check_right", "user_presence", "user_project_presence"]

    def process(self):
        self._delete()
        self.remove_from_task()
        return self

    def _delete(self):
        self._user_project.delete()

    def remove_from_task(self):
        self._user.tasks_user.filter(task__project_id=self.cleaned_data['id']).delete()

    @property
    @lru_cache
    def _user(self):
        try:
            return User.objects.get(id=self.cleaned_data['user_id'])
        except User.DoesNotExist:
            return None

    @property
    @lru_cache
    def _user_project(self):
        try:
            return UserProject.objects.get(
                user=self._user,
                project_id=self.cleaned_data['id']
            )
        except UserProject.DoesNotExist:
            return None

    def check_right(self):
        if not UserProject.objects.filter(
                user=self.cleaned_data['user'],
                project_id=self.cleaned_data['id']
        ) or self.cleaned_data['user'].role != User.manager:
            raise PermissionDenied("PermissionDenied")

    def user_project_presence(self):
        if not self._user_project:
            raise NotFound("UserProject with this parms not found")

    def user_presence(self):
        if not self._user:
            raise NotFound("User with this id not found")