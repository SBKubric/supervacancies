from django.http import HttpRequest

from supervacancies.vacancies import services


def user_settings(request: HttpRequest) -> dict:
    if request.user.is_anonymous:
        return dict()

    return {
        "user": request.user,
        "user_has_no_company": services.check_user_has_no_companies(
            request.user  # type: ignore
        ),
        "user_has_no_cv": services.check_user_has_no_cv(request.user),  # type: ignore
    }
