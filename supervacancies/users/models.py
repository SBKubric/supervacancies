from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    """
    Base user model for SuperVacancies.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    
    @property
    def is_employer(self):
        return self.has_perm('users.access_employer_area')

    @property
    def is_applicant(self):
        return self.has_perm('users.access_applicant_area')

    @property
    def has_no_company(self):
        return self.legalentity_set.count() == 0

    @property
    def has_no_cv(self):
        return self.cv_set.count() == 0

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


def set_applicant_group(user: User) -> None:
    """
    Sets user permissions at sign up if user role selected as applicant.
    """
    if user.has_perm('users.access_applicant_area'):
        return

    applicants_group, _ = Group.objects.get_or_create(name="applicants")

    content_type = ContentType.objects.get_for_model(User)
    applicant_permission = Permission.objects.get(
        codename = "access_applicant_area",
        content_type = content_type, 
    )

    if applicant_permission not in applicants_group.permissions.all():
        applicants_group.permissions.add(applicant_permission)
    
    user.groups.add(applicants_group) # type: ignore



def set_employer_group(user: User) -> None:
    """
    Sets user permissions at sign up if user role is selected as employer
    """
    if user.has_perm('users.access_employer_area'):
        return
    employers_group, _ = Group.objects.get_or_create(name="employers")
    content_type = ContentType.objects.get_for_model(User)
    employer_permission = Permission.objects.get(
        codename = "access_employer_area",
        content_type = content_type, 
    )

    if employer_permission not in employers_group.permissions.all():
        employers_group.permissions.add(employer_permission)

    user.groups.add(employers_group) # type: ignore

