from django.urls import path

from api.views.main import MainPageView

urlpatterns = [
    path("", MainPageView.as_view(), name='index')
]

