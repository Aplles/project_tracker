from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.task.append_member import TaskMemberAppendService
from api.services.task.change import TaskChangeService
from api.services.task.create import TaskCreateService
from api.services.task.delete import TaskDeleteService
from api.services.task.remove_member import TaskMemberDeleteService


class TaskCreateView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        ServiceOutcome(
            TaskCreateService,
            kwargs | request.POST.dict() | {"user": request.user}
        )
        return redirect('project_page', **kwargs)


class TaskChangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ServiceOutcome(TaskChangeService, request.data | kwargs)
        return Response({})


class TaskDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ServiceOutcome(TaskDeleteService, request.data | kwargs | {"user": request.user})
        return Response({})


class TaskMemberDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ServiceOutcome(TaskMemberDeleteService, request.data | kwargs | {"user": request.user})
        return Response({})


class TaskMemberAppendView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        ServiceOutcome(TaskMemberAppendService, request.data | kwargs | {"user": request.user})
        return Response({})
