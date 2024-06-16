from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from service_objects.errors import InvalidInputsError
from service_objects.services import ServiceOutcome

from api.serializers.user_project.list import UserProjectListSerializer
from api.services.project.create import ProjectCreateService
from models_app.models import UserProject, Dashboard, Project, TaskUser, Task, Timer


class UserProjectListView(ListAPIView):
    serializer_class = UserProjectListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        projects = UserProject.objects.filter(user=self.request.user)
        search = self.request.GET.get("search", "")
        if search:
            projects = projects.filter(project__name__icontains=search)
        return projects


class ProjectPageView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs["id"])
        search_query = request.GET.get('search', '')
        my_task = request.GET.get('my_task', '')
        dashboards = Dashboard.objects.prefetch_related(
            'tasks_status', "tasks_status__author"
        ).filter(project=project).order_by('position')

        for dashboard in dashboards:
            if search_query:
                dashboard.tasks_status_filtered = dashboard.tasks_status.filter(
                    Q(title__icontains=search_query) | Q(description__icontains=search_query)
                )
            else:
                dashboard.tasks_status_filtered = dashboard.tasks_status.all()

            if my_task:
                dashboard.tasks_status_filtered = dashboard.tasks_status_filtered.filter(
                    id__in=TaskUser.objects.filter(user=request.user).values_list('task_id', flat=True)
                )

            dashboard.tasks_status_filtered = dashboard.tasks_status_filtered.annotate(
                total_time=Sum(F('tasks_task__timers_task_user__result_time'))
            )
            dashboard.count_task = dashboard.tasks_status_filtered.count()

        return render(request, 'home.html', context={
            'status': dashboards,
            'project': project,
            'search': search_query,
            'my_task': my_task
        })


class ProjectCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(ProjectCreateService, request.POST.dict() | {"user": request.user}, request.FILES)
        except InvalidInputsError as e:
            return redirect(request.META.get("HTTP_REFERER", ""))
        return redirect('project_page', id=outcome.result.id)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('auth')

    model = Project
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ProjectStatisticView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('auth')
    template_name = 'statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(id=kwargs['id'])
        context["project"] = project

        task_stats = []
        total_time_spent = timedelta()

        tasks = Task.objects.filter(project=project)
        for task in tasks:
            user_stats = []
            task_total_time_spent = timedelta()
            task_users = TaskUser.objects.filter(task=task)
            for task_user in task_users:
                user_time_spent = timedelta()
                timers = Timer.objects.filter(task_user=task_user)
                for timer in timers:
                    if timer.result_time:
                        user_time_spent += timer.result_time
                        task_total_time_spent += timer.result_time

                user_stats.append({
                    'user': task_user.user,
                    'time_spent': user_time_spent
                })

            if task_total_time_spent:
                task_stats.append({
                    'task': task,
                    'user_stats': user_stats,
                    'total_time_spent': task_total_time_spent
                })
            total_time_spent += task_total_time_spent

        context['task_stats'] = task_stats
        context['total_time_spent'] = total_time_spent

        return context
