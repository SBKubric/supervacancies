from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from container import get_local_user
from .exceptions import LoginRequiredError
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _


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
        proxy = True


class LegalEntity(BaseModel):
    title = models.CharField(_("Title"))
    description = models.TextField(_("Description"), blank=True)
    size = models.SmallIntegerField(_("Number of employees"), blank=True)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField(_("Phone"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    address1 = models.CharField(_("Address 1"), blank=True)
    address2 = models.CharField(_("Address 2"), blank=True)
    city = models.CharField(_("City"), blank=True)
    postal_code = models.CharField(_("Postal code"), blank=True)
    country = models.CharField(_("Country"), blank=True)


class Vacancy(BaseModel):
    title = models.CharField(_("Title"))
    description = models.TextField(_("Description"), blank=True)
    status = models.CharField(_("Status"))
    salary = MoneyField(
        _("Salary"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD", # type: ignore
        blank=True,
    )
    required_experience = models.SmallIntegerField(_("Years of experience"))
    employer = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(LegalEntity, on_delete=models.CASCADE)


class CV(BaseModel):
    title = models.CharField(_("Title"))
    description = models.TextField(_("Description"), blank=True)
    status = models.CharField(_("Status"))
    salary = MoneyField(
        _("Salary"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD", # type: ignore
        blank=True,
    )
    phone = PhoneNumberField(_("Contact phone"))
    email = models.EmailField(_("Contact email"))
    experience = models.TextField(_("Experience"))
    applicant = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)


class Application(BaseModel):
    status = models.CharField(_("Status"))
    cover_letter = models.TextField(_("Cover letter"), blank=True)
    applicant = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)


