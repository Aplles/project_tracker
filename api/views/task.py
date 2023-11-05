from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from service_objects.services import ServiceOutcome

from api.services.task.create import TaskCreateService


class TaskCreateView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        ServiceOutcome(
            TaskCreateService,
            kwargs | request.POST.dict() | {"user": request.user}
        )
        return redirect('project_page', **kwargs)
