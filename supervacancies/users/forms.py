from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import fields
from django.utils.translation import gettext_lazy as _
from polog import log

from .enums import UserRoles

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


@log("Saving user...", methods=("save",))  # type: ignore
class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    User is created based on role.

    If role has unexpected value or not provided, we log UserRoleBadError.

    Check UserSocialSignupForm for accounts created from social.
    """

    role = fields.TypedChoiceField(
        choices=UserRoles.choices, label=_("Choose your role"), coerce=int
    )


@log("Saving user...", methods=("save",))  # type: ignore
class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.

    If role has unexpected value or not provided, we log UserRoleBadError.


    See UserSignupForm otherwise.
    """

    role = fields.TypedChoiceField(
        choices=UserRoles.choices, label=_("Choose your role"), coerce=int
    )
