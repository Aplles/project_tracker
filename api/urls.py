from django.urls import path

from api.views.main import IndexPageView, HomePageView
from api.views.project import UserProjectListView, ProjectPageView

urlpatterns = [
    # API
    path("user/projects/", UserProjectListView.as_view(), name='list_projects'),


    # Pages
    path("", IndexPageView.as_view(), name='index'),
    path("home/", HomePageView.as_view(), name='home'),
    path("home/project/<id>/", ProjectPageView.as_view(), name='project_page'),
]

