from django.shortcuts import redirect
from django.views import View
from service_objects.services import ServiceOutcome

from api.services.dashboard.change import DashboardChangeService
from api.services.dashboard.create import DashboardCreateService
from api.services.dashboard.delete import DashboardDeleteService


class DashboardCreateView(View):

    def post(self, request, *args, **kwargs):
        ServiceOutcome(DashboardCreateService, request.POST.dict() | kwargs)
        return redirect('project_page', **kwargs)


class DashboardChangeView(View):

    def post(self, request, *args, **kwargs):
        ServiceOutcome(DashboardChangeService, request.POST.dict() | kwargs)
        return redirect('project_page', id=kwargs["project_id"])


class DashboardDeleteView(View):

    def post(self, request, *args, **kwargs):
        ServiceOutcome(DashboardDeleteService, request.POST.dict() | kwargs)
        return redirect('project_page', id=kwargs["project_id"])
