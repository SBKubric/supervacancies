from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import EmployerUser, ApplicantUser

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class EmployerUserSignupForm(SignupForm):
    """
    Form that will be rendered on a employer sign up section/screen.
    Default fields will be added automatically.
    Check EmployerUserSocialSignupForm for accounts created from social.
    """

    class Meta:
        model = EmployerUser


class ApplicantUserSignupForm(SignupForm):
    """
    Form that will be rendered on a applicant sign up section/screen.
    Default fields will be added automatically.
    Check ApplicantUserSocialSignupForm for accounts created from social.
    """

    class Meta:
        model = EmployerUser


class EmployerUserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See EmployerUserSignupForm otherwise.
    """

class ApplicantUserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See ApplicantUserSignupForm otherwise.
    """
