from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from service_objects.errors import ServiceObjectLogicError
from service_objects.services import ServiceOutcome

from api.services.user.auth import UserAuthService


def logout_user(request):
    """Log out"""
    logout(request)
    return redirect('index')


class UserAuthView(View):

    def get(self, request, *args, **kwargs):
        errors = request.session.get("errors", '')
        if errors:
            del request.session['errors']
        return render(request, 'auth.html', context={
            'errors': errors
        })

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                UserAuthService, request.POST.dict() | {"request": request}
            )
        except ServiceObjectLogicError as e:
            request.session['errors'] = e.errors_dict
            return redirect('auth')
        login(request, outcome.result)
        return redirect('home')
