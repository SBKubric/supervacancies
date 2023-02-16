from django.contrib.auth.mixins import UserPassesTestMixin


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
