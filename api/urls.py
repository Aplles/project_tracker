from django.urls import path

from api.views.main import IndexPageView, HomePageView
from api.views.project import UserProjectListView, ProjectPageView, ProjectCreateView
from api.views.subtask import SubTaskCreateView
from api.views.task import TaskCreateView, TaskChangeView
from api.views.user import logout_user, UserAuthView

urlpatterns = [
    # API
    path("user/projects/", UserProjectListView.as_view(), name="list_projects"),
    path("project/<int:id>/subtask/create/", SubTaskCreateView.as_view(), name="create_subtask"),
    path("project/<int:id>/task/change/", TaskChangeView.as_view(), name="change_task"),
    path("project/create/", ProjectCreateView.as_view(), name="create_task"),

    # Pages
    path("", IndexPageView.as_view(), name="index"),
    path("home/", HomePageView.as_view(), name="home"),
    path("home/project/<int:id>/", ProjectPageView.as_view(), name="project_page"),
    path("project/<int:id>/task/create/", TaskCreateView.as_view(), name="create_task"),

    path("user/logout/", logout_user, name="logout"),
    path("user/auth/", UserAuthView.as_view(), name="auth"),
]
