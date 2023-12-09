from django.shortcuts import redirect
from django.views import View
from service_objects.services import ServiceOutcome

from api.services.dashboard.create import DashboardCreateService


class DashboardCreateView(View):

    def post(self, request, *args, **kwargs):
        ServiceOutcome(DashboardCreateService, request.POST.dict() | kwargs)
        return redirect('project_page', **kwargs)
