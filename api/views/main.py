from django.shortcuts import render
from django.views import View

from models_app.models import Project


class MainPageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={
            'projects': Project.objects.all()[:5]
        })
