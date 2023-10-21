from django.shortcuts import render
from django.views import View

from models_app.models import Project


class IndexPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={
            'projects': Project.objects.all()[:5]
        })


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
