from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserRoles(IntegerChoices):
    EMPLOYER = 1, _("Employer")
    APPLICANT = 2, _("Applicant")
