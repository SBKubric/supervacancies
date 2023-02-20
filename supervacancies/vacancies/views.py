from typing import Any

from django.conf import settings
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.views import generic

from supervacancies.users import permissions
from supervacancies.vacancies import models, services

from . import enums

PAGINATE_BY = settings.PAGINATE_BY


class VacanciesView(generic.ListView):
    model = models.Vacancy
    paginate_by = PAGINATE_BY
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["jobs"] = models.Job.objects.all()
        return context

    def get_queryset(self) -> QuerySet:
        return models.Vacancy.objects.all().prefetch_related()


class SearchVacanciesView(VacanciesView):
    pass


class CreateVacancyView(permissions.UserIsEmployerMixin, generic.CreateView):
    template_name_suffix = "_create_form"
    model = models.Vacancy
    fields = ["company", "title", "job", "description", "required_experience", "salary"]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.create_vacancy(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class UpdateVacancyView(permissions.UserIsEmployerMixin, generic.UpdateView):
    model = models.Vacancy
    fields = ["title", "job", "description", "required_experience", "salary"]


class DetailVacancyView(generic.DetailView):
    model = models.Vacancy


class ArchiveVacancyView(permissions.UserIsEmployerMixin, generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.Vacancy
    fields = []


class RegisterLegalEntityView(permissions.UserIsEmployerMixin, generic.CreateView):
    template_name_suffix = "_register_form"
    model = models.LegalEntity
    fields = [
        "title",
        "description",
        "size",
        "phone",
        "email",
        "address1",
        "address2",
        "city",
        "postal_code",
        "country",
    ]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.register_legal_entity(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class DetailLegalEntityView(generic.DetailView):
    model = models.LegalEntity


class UpdateLegalEntityView(permissions.UserIsEmployerMixin, generic.UpdateView):
    model = models.LegalEntity
    template_name_suffix = "_update_form"
    fields = [
        "title",
        "description",
        "size",
        "phone",
        "email",
        "address1",
        "address2",
        "city",
        "postal_code",
        "country",
    ]


class ArchiveLegalEntityView(permissions.UserIsEmployerMixin, generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.LegalEntity
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.archive_legal_entity(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class CreateCVView(permissions.UserIsApplicantMixin, generic.CreateView):
    template_name_suffix = "_create_form"
    model = models.CV
    fields = [
        "title",
        "job",
        "description",
        "salary",
        "phone",
        "email",
        "experience",
        "experience_description",
        "cv_file",
    ]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.create_cv(self, form)
        return HttpResponseRedirect(reverse("vacancies:applicant"))


class UpdateCVView(permissions.UserIsApplicantMixin, generic.UpdateView):
    template_name_suffix = "_update_form"
    model = models.CV
    fields = [
        "title",
        "job",
        "description",
        "salary",
        "phone",
        "email",
        "experience",
        "experience_description",
        "cv_file",
    ]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.update_cv(self, form)
        return HttpResponseRedirect(reverse("vacancies:applicant"))


class ArchiveCVView(permissions.UserIsApplicantMixin, generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.CV
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.archive_cv(self, form)
        return HttpResponseRedirect(reverse("vacancies:applicant"))


class DetailCVView(generic.DetailView):
    model = models.CV


class SubmitApplicationView(permissions.UserIsApplicantMixin, generic.CreateView):
    template_name_suffix = "_submit_form"
    model = models.Application
    fields = [
        "cover_letter",
        "cv",
    ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["vacancy"] = models.Vacancy.objects.get(
            id=self.kwargs.get("vacancy_id")
        )
        return context

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.submit_application(self, form)
        return HttpResponseRedirect(reverse("vacancies:applicant"))


class AcceptApplicationView(permissions.UserIsEmployerMixin, generic.UpdateView):
    template_name_suffix = "_check_accept"
    model = models.Application
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.accept_application(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class RejectApplicationView(permissions.UserIsEmployerMixin, generic.UpdateView):
    template_name_suffix = "_check_reject"
    model = models.Application
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.reject_application(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class EmployerCockpitView(permissions.UserIsEmployerMixin, generic.ListView):
    template_name = "vacancies/employer_cockpit.html"
    model = models.Vacancy
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["legal_entities"] = self.request.user.legalentity_set.all()  # type: ignore
        return context

    def get_queryset(self) -> QuerySet:
        return self.request.user.vacancy_set.all()  # type: ignore


class ApplicantCockpitView(permissions.UserIsApplicantMixin, generic.ListView):
    template_name = "vacancies/applicant_cockpit.html"
    model = models.Application
    paginate_by = PAGINATE_BY

    def get_queryset(self) -> QuerySet:
        return self.request.user.application_set.filter(  # type: ignore
            status=enums.ApplicationStatuses.ACTIVE
        ).all()  # type: ignore
