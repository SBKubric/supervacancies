from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

from supervacancies.container import get_local_user
from supervacancies.vacancies import enums

from .exceptions import LoginRequiredError

USER_MODEL = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        USER_MODEL, related_name="+", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        USER_MODEL, related_name="+", on_delete=models.CASCADE
    )

    def save(self):
        """Overriding save method to set user that created and changed models"""
        user = get_local_user()

        if not user or not user.is_authenticated:
            raise LoginRequiredError

        self.updated_by = user
        if self._state.adding:
            self.created_by = user
        super().save()

    class Meta:
        abstract = True


class LegalEntity(BaseModel):
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=enums.LegalEntityStatuses.ACTIVE,
        choices=enums.LegalEntityStatuses.choices,
    )
    size = models.PositiveSmallIntegerField(
        _("Number of employees"),
        default=enums.CompanySizes.MEDIUM,
        choices=enums.CompanySizes.choices,
    )
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField(_("Phone"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    address1 = models.CharField(_("Address 1"), blank=True, max_length=255)
    address2 = models.CharField(_("Address 2"), blank=True, max_length=255)
    city = models.CharField(_("City"), blank=True, max_length=100)
    postal_code = models.CharField(_("Postal code"), blank=True, max_length=50)
    country = models.CharField(_("Country"), blank=True, max_length=100)

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "id"], name="%(app_label)s_%(class)s_status"
            ),
        ]

    def __str__(self) -> str:
        return str(self.title)


class Vacancy(BaseModel):
    title = models.CharField(_("Title"), max_length=100)
    job = models.ForeignKey(
        "Job", on_delete=models.SET_NULL, null=True
    )  # on delete set as "no job"
    description = models.TextField(_("Description"), blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=enums.VacancyStatuses.ACTIVE,
        choices=enums.VacancyStatuses.choices,
    )
    salary = MoneyField(
        _("Salary"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD",  # type: ignore
        null=True,
        blank=True,
    )
    required_experience = models.PositiveSmallIntegerField(
        _("Years of experience"),
        default=enums.ExperienceRequirements.NO,
        choices=enums.ExperienceRequirements.choices,
    )
    employer = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(LegalEntity, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "id"], name="%(app_label)s_%(class)s_status"
            ),
        ]


class CV(BaseModel):
    title = models.CharField(_("Title"), max_length=100)
    job = models.ForeignKey(
        "Job", on_delete=models.SET_NULL, null=True
    )  # on delete set as "no job"
    description = models.TextField(_("Description"), blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=enums.CVStatuses.ACTIVE,
        choices=enums.CVStatuses.choices,
    )
    salary = MoneyField(
        _("Salary"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD",  # type: ignore
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(_("Contact phone"))
    email = models.EmailField(_("Contact email"))
    experience = models.PositiveSmallIntegerField(
        _("Years of experience"),
        default=enums.ExperienceRequirements.NO,
        choices=enums.ExperienceRequirements.choices,
    )
    experience_description = models.TextField(_("Experience"), blank=True)
    applicant = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    cv_file = models.FileField(_("CV file"), null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "id"], name="%(app_label)s_%(class)s_status"
            ),
        ]

    def __str__(self):
        return str(self.title)


class Application(BaseModel):
    state = models.PositiveBigIntegerField(
        default=enums.ApplicationStates.PENDING,
        choices=enums.ApplicationStates.choices,
    )
    status = models.PositiveSmallIntegerField(
        _("Status"),
        default=enums.ApplicationStatuses.ACTIVE,
        choices=enums.ApplicationStatuses.choices,
    )
    cover_letter = models.TextField(_("Cover letter"), blank=True)
    applicant = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    cv_file = models.FileField(
        _("Your CV file"),
        upload_to="cv",
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "id"], name="%(app_label)s_%(class)s_status"
            ),
            models.Index(
                fields=["state", "status", "id"],
                name="%(app_label)s_%(class)s_state",
            ),
        ]


class Job(models.Model):
    """
    Dictionary with different jobs.
    """

    title = models.CharField(_("Job name"), max_length=100)

    def __str__(self) -> str:
        return str(self.title)
