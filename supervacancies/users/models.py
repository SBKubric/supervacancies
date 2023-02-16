from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager, AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from typing import Any


class User(AbstractUser):
    """
    Base user model for SuperVacancies.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        permissions = [
            ("access_employer_area", "Is user an employer?"),
            ("access_applicant_area", "Is user an applicant?")
        ]


class EmployerUserManager(UserManager):
    """
    User manager for employers.
    """
    def create_user(self, username: str, email: str | None, password: str | None, **extra_fields: Any) -> User:
        """Method for creation of user with applicant group permissions
        Returns:
            AbstractUser: User with employer group permissions
        """
        employer: User = super().create_user(username, email, password, **extra_fields)
        
        employers_group, _ = Group.objects.get_or_create(name="employers")
        content_type = ContentType.objects.get_for_model(User)
        employer_permission = Permission.objects.get(
            codename = "access_employer_area",
            content_type = content_type, 
        )

        if employer_permission not in employers_group.permissions.all():
            employers_group.permissions.add(employer_permission)

        employers_group.user_set.add(employer) # type: ignore
        employers_group.save()

        return employer
    


class ApplicantUserManager(UserManager):
    """
    User manager for applicants.
    """
    def create_user(self, username: str, email: str | None, password: str | None, **extra_fields: Any) -> User:
        """Method for creation user with applicant group permissions
        Returns:
            User: User with applicant group permissions
        """

        applicant: User = super().create_user(username, email, password, **extra_fields)
        applicants_group, _ = Group.objects.get_or_create(name="applicants")

        content_type = ContentType.objects.get_for_model(User)
        applicant_permission = Permission.objects.get(
            codename = "access_applicant_area",
            content_type = content_type, 
        )

        if applicant_permission not in applicants_group.permissions.all():
            applicants_group.permissions.add(applicant_permission)

        applicants_group.user_set.add(applicant) # type: ignore
        applicants_group.save()

        return applicant


class EmployerUser(User):
    """
    User in the employers group
    """

    objects = EmployerUserManager()

    class Meta:
        proxy = True


class ApplicantUser(User):
    """
    User in the applicants group
    """
    objects = ApplicantUserManager()

    class Meta:
        proxy = True
