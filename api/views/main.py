from django.shortcuts import render, redirect
from django.views import View
from rest_framework.exceptions import ValidationError
from service_objects.services import ServiceOutcome

from api.services.invite.invite import InviteService
from models_app.models import Project


class IndexPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={
            'projects': Project.objects.all()[:5]
        })


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("auth")
        return render(request, 'home.html')


class InviteView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        try:
            outcome = ServiceOutcome(InviteService, kwargs | {"user": request.user})
        except (ValidationError, ) as e:
            return redirect("index")
        return redirect('project_page', outcome.result.id)
