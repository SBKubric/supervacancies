from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from typing import Callable


class UserIsEmployerMixin(UserPassesTestMixin):
    """
    Class for restricting access to views, meant for employer-only use
    """
    def test_func(self) -> bool | None:
        return self.request.user.has_perm('users.access_employer_area')  # type: ignore


class UserIsApplicantMixin(UserPassesTestMixin):
    """
    Class for restricting access to views, meant for applicant-only use
    """
    def test_func(self) -> bool | None:
        return self.request.user.has_perm('users.access_applicant_area') # type: ignore


def employer_required(func: Callable, redirect_url=None) -> Callable:
    actual_dec = user_passes_test(
        lambda u: u.has_perm('users.access_employer_area'), # type: ignore
        redirect_url
    )
    if func:
        return actual_dec(func)

    return actual_dec


def applicant_required(func: Callable, redirect_url=None) -> Callable:
    actual_dec = user_passes_test(
        lambda u: u.has_perm('users.access_applicant_area'), # type: ignore
        redirect_url
    )
    if func:
        return actual_dec(func)

    return actual_dec
