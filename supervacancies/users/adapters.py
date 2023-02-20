from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from .enums import UserRoles
from .models import set_employer_group, set_applicant_group


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True): 
        user = super().save_user(request, user, form, commit)

        if not commit:
            return user

        user_role = form.cleaned_data.get("role")
        match user_role:
            case UserRoles.EMPLOYER:
                set_employer_group(user)
            case UserRoles.APPLICANT:
                set_applicant_group(user)
            case _:
               pass

        return user




class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        if not form:
            return user
        
        user_role = form.cleaned_data.get("role")

        match user_role:
            case UserRoles.EMPLOYER:
                set_employer_group(user)
            case UserRoles.APPLICANT:
                set_applicant_group(user)
            case _:
               pass 

        return user

