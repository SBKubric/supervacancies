from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class CompanySizes(IntegerChoices):
    TINY = 0, _("Less than 10 people")
    SMALL = 1, _("Less than 30 people")
    MEDIUM = 2, _("Between 30 and 100 people")
    LARGE = 3, _("Between 100 and 1000 people")
    XLARGE = 4, _("Between 1000 and 5000 people")
    CORPORATION = 5, _("More than 5000 people")


class ApplicationStatuses(IntegerChoices):
    PENDING = 0, _("Awaits response")
    APPROVED = 1, _("Empoyer approved application")
    REJECTED = 2, _("Employer rejected application")


class CVStatuses(IntegerChoices):
    ACTIVE = 0, _("Visible")
    ARCHIVED = 1, _("In archive")


class VacancyStatuses(IntegerChoices):
    ACTIVE = 0, _("Looking for candidates")
    ARCHIVED = 1, _("In archive")


class ExperienceRequirements(IntegerChoices):
    NO = 0, _("No experience"),
    JUNIOR = 1, _("From 6 month to 1 year"),
    JUNIOR_PLUS = 2, _("From 1 year to 3 years"),
    MIDDLE = 3, _("From 3 to 6 years"),
    SENIOR = 4, _("More than 6 years")

