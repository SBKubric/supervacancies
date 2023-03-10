from django.contrib.auth import get_user

from supervacancies.container import reset_local_user, set_local_user


class SetLocalUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = get_user(request)
        set_local_user(user)
        response = self.get_response(request)
        reset_local_user()  # Need to clear current user to avoid clashes
        return response
