from django.db.models import Count
from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.user_project.list import UserProjectListSerializer
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
