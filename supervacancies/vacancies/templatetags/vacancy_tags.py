from typing import Any

from django.template import Library

from supervacancies.vacancies.models import Vacancy
from supervacancies.vacancies.services import check_user_has_no_application

register = Library()


@register.simple_tag(takes_context=True)
def set_vacancy_context(context: dict[str, Any], vacancy: Vacancy):
    context["no_application"] = False
    user = context["user"]
    if user.is_applicant and check_user_has_no_application(user, vacancy):
        context["no_application"] = True
    return ""
