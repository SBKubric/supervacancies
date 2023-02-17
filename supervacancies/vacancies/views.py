from django.views import generic
from .models import Vacancy, LegalEntity, CV, Application, Job
from django.db.models import QuerySet
from django.conf import settings
from typing import Any

PAGINATE_BY = settings.PAGINATE_BY

# Create your views here.

class VacanciesView(generic.ListView):
    model = Vacancy
    paginate_by = PAGINATE_BY
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        return context

    def get_queryset(self) -> QuerySet:
      return Vacancy.objects.all().prefetch_related()


class SearchVacanciesView(generic.ListView):
    paginate_by = PAGINATE_BY
    model = Vacancy
    template_name = "vacancies/vacancies.html"

    def get_queryset(self) -> QuerySet:
        return Vacancy.objects.all()


class CreateVacancyView(generic.CreateView):
    template_name_suffix = "_create_form"
    model = Vacancy
    fields = ['company', 'title', 'job', 'description', 'required_experience', 'salary']


class UpdateVacancyView(generic.UpdateView):
    model = Vacancy
    fields = ['title', 'job', 'description', 'required_experience', 'salary']


class ArchiveVacancyView(generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = Vacancy
    fields = []


class RegisterLegalEntityView(generic.CreateView):
    template_name_suffix = "_register_form"
    model = LegalEntity
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

    def form_valid(self, form: _ModelFormT) -> HttpResponse:
        form.
        return super().form_valid(form)


class UpdateLegalEntityView(generic.UpdateView):
    model = LegalEntity
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
    model = LegalEntity
    fields = []


class CreateCVView(generic.CreateView):
    template_name_suffix = "_create_form"
    model = CV
    fields = [
        'title', 
        'job', 
        'description', 
        'salary', 
        'phone', 
        'email', 
        'experience', 
        'experience_description'
    ]


class UpdateCVView(generic.UpdateView):
    template_name_suffix = "_update_form"
    model = CV
    fields = [
        'title', 
        'job', 
        'description', 
        'salary', 
        'phone', 
        'email', 
        'experience', 
        'experience_description'
    ]



class ArchiveCVView(generic.UpdateView):
    template_name_suffix = "_check_archive"
    model = CV
    fields = []


class SubmitApplicationView(generic.CreateView):
    template_name_suffix = "_submit_form"
    model = Application
    fields = [
        'cover_letter',
        'cv_file',
    ]


class AcceptApplicationView(generic.UpdateView):
    template_name_suffix = "_check_accept"
    model = Application
    fields = []


class RejectApplicationView(generic.UpdateView):
    template_name_suffix = "_check_reject"
    model = Application
    fields = []


class EmployerCockpitView(generic.ListView):
    template_name = "vacancies/employer_cockpit.html"
    model = Vacancy

    def get_queryset(self) -> QuerySet:
        return self.request.user.vacancy_set.all()


class ApplicantCockpitView(generic.ListView):
    template_name = "vacancies/applicant_cockpit.html"
    model = Application

    def get_queryset(self) -> QuerySet:
        return self.request.user.application_set.all()

