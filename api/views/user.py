from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.views import View
from service_objects.services import ServiceOutcome

from api.services.user.auth import UserAuthService


def logout_user(request):
    """Log out"""
    logout(request)
    return redirect('index')


class UserAuthView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'auth.html', context={

        })

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserAuthService, request.data)
        return render(request, 'auth.html', context={

        })
