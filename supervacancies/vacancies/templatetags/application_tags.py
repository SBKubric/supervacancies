from typing import Any
from django.template import Library
from supervacancies.vacancies.models import Application
from supervacancies.vacancies.enums import ApplicationStates
register = Library()


@register.simple_tag(takes_context=True)
def set_application_context(context: dict[str, Any], application: Application):
    context['application_state_accepted'] = application.state == ApplicationStates.ACCEPTED
    context['application_state_rejected'] = application.state == ApplicationStates.REJECTED
    return ""
