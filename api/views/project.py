from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from service_objects.errors import InvalidInputsError
from service_objects.services import ServiceOutcome

from api.serializers.user_project.list import UserProjectListSerializer
from api.services.project.create import ProjectCreateService
from models_app.models import UserProject, Dashboard, Project


class UserProjectListView(ListAPIView):
    queryset = UserProject.objects.all()
    serializer_class = UserProjectListSerializer
    permission_classes = (IsAuthenticated,)


class ProjectPageView(View):

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["id"])
        return render(request, 'home.html', context={
            'status': Dashboard.objects.prefetch_related('tasks_status').annotate(
                count_task=Count('tasks_status')
            ).filter(project=project).order_by('position'),
            'project': project,
        })


class ProjectCreateView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(ProjectCreateService, request.POST.dict() | {"user": request.user}, request.FILES)
        except InvalidInputsError as e:
            return redirect(request.META.get("HTTP_REFERER", ""))
        return redirect('project_page', id=outcome.result.id)
