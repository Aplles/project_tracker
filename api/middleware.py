from django.shortcuts import redirect
from django.urls import reverse


class CheckUserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.path.startswith('/admin'):
            if not request.user.first_name or not request.user.last_name:
                allowed_paths = [
                    reverse('home'),  # Главная страница
                    reverse('logout'),  # Разрешаем выход
                    reverse('list_projects'),
                    reverse('index'),
                    reverse('profile'),
                ]
                if request.path not in allowed_paths:
                    return redirect('home')

        response = self.get_response(request)
        return response
