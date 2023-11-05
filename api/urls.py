from django.urls import path

from api.views.main import IndexPageView, HomePageView
from api.views.project import UserProjectListView, ProjectPageView
from api.views.subtask import SubTaskCreateView
from api.views.task import TaskCreateView

urlpatterns = [
    # API
    path("user/projects/", UserProjectListView.as_view(), name='list_projects'),
    path("project/<id>/subtask/create/", SubTaskCreateView.as_view(), name='create_subtask'),


    # Pages
    path("", IndexPageView.as_view(), name='index'),
    path("home/", HomePageView.as_view(), name='home'),
    path("home/project/<id>/", ProjectPageView.as_view(), name='project_page'),
    path("project/<id>/task/create/", TaskCreateView.as_view(), name='create_task'),
]

