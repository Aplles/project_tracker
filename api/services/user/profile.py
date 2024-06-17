from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import User


class UserProfileService(ServiceWithResult):
    user = ModelField(User)
    first_name = forms.CharField()
    last_name = forms.CharField()
    avatar = forms.ImageField(required=False)
    role = forms.CharField()

    def process(self):
        self._change()
        return self

    def _change(self):
        user = self.cleaned_data['user']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.avatar = self.cleaned_data['avatar']
        user.role = self.cleaned_data['role']
        user.save()

