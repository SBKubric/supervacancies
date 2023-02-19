from django.views import generic
from supervacancies.vacancies import models
from supervacancies.vacancies import services
from django.db.models import QuerySet
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from typing import Any
from django.shortcuts import reverse


PAGINATE_BY = settings.PAGINATE_BY


class VacanciesView(generic.ListView):
    model = models.Vacancy
    paginate_by = PAGINATE_BY
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['jobs'] = models.Job.objects.all()
        return context

    def get_queryset(self) -> QuerySet:
      return models.Vacancy.objects.all().prefetch_related()


class SearchVacanciesView(generic.ListView):
    paginate_by = PAGINATE_BY
    model = models.Vacancy
    template_name = "vacancies/vacancies.html"

    def get_queryset(self) -> QuerySet:
        return models.Vacancy.objects.all()


class CreateVacancyView(generic.CreateView):
    template_name_suffix = "_create_form"
    model = models.Vacancy
    fields = ['company', 'title', 'job', 'description', 'required_experience', 'salary']


class UpdateVacancyView(generic.UpdateView):
    model = models.Vacancy
    fields = ['title', 'job', 'description', 'required_experience', 'salary']


class DetailVacancyView(generic.DetailView):
    model = models.Vacancy


class ArchiveVacancyView(generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.Vacancy
    fields = []


class RegisterLegalEntityView(generic.CreateView):
    template_name_suffix = "_register_form"
    model = models.LegalEntity
    fields = [
        'title', 
        'description', 
        'size', 
        'phone', 
        'email', 
        'address1', 
        'address2',
        'city',
        'postal_code',
        'country',
    ]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.register_legal_entity(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class UpdateLegalEntityView(generic.UpdateView):
    model = models.LegalEntity
    fields = [
        'title', 
        'description', 
        'size', 
        'phone', 
        'email', 
        'address1', 
        'address2',
        'city',
        'postal_code',
        'country',
    ]


class ArchiveLegalEntityView(generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.LegalEntity
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.archive_legal_entity(self, form)
        return HttpResponseRedirect(reverse("vacancies:employer"))


class CreateCVView(generic.CreateView):
    template_name_suffix = "_create_form"
    model = models.CV
    fields = [
        'title', 
        'job', 
        'description', 
        'salary', 
        'phone', 
        'email', 
        'experience', 
        'experience_description',
        'cv_file',
    ]
    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.create_cv(self, form)
        return HttpResponseRedirect(reverse("vacancies:applicant"))


class UpdateCVView(generic.UpdateView):
    template_name_suffix = "_update_form"
    model = models.CV
    fields = [
        'title', 
        'job', 
        'description', 
        'salary', 
        'phone', 
        'email', 
        'experience', 
        'experience_description',
        'cv_file'
    ]
    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.update_cv(self, form)
        return HttpResponseRedirect(
            reverse('vacancies:applicant')
        )


class ArchiveCVView(generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = models.CV
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.archive_cv(self, form)
        return HttpResponseRedirect(
            reverse('vacancies:applicant')
        )


class DetailCVView(generic.DetailView):
    model = models.CV


class SubmitApplicationView(generic.CreateView):
    template_name_suffix = "_submit_form"
    model = models.Application
    fields = [
        'cover_letter',
        'cv_file',
    ]
    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.submit_application(self, form)
        return super().form_valid(form)


class AcceptApplicationView(generic.UpdateView):
    template_name_suffix = "_check_accept"
    model = models.Application
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.accept_application(self, form)
        return HttpResponseRedirect(
            reverse("vacancies:employer")
        )


class RejectApplicationView(generic.UpdateView):
    template_name_suffix = "_check_reject"
    model = models.Application
    fields = []

    def form_valid(self, form: ModelForm) -> HttpResponse:
        services.reject_application(self, form)
        return HttpResponseRedirect(
            reverse("vacancies:employer")
        )


class EmployerCockpitView(generic.ListView):
    template_name = "vacancies/employer_cockpit.html"
    model = models.Vacancy

    def get_queryset(self) -> QuerySet:
        return self.request.user.vacancy_set.all() # type: ignore


class ApplicantCockpitView(generic.ListView):
    template_name = "vacancies/applicant_cockpit.html"
    model = models.Application

    def get_queryset(self) -> QuerySet:
        return self.request.user.application_set.all() # type: ignore

