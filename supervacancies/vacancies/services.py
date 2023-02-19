from . import models
from . import enums
from django.db.transaction import atomic
from django.db.models.fields.files import FieldFile
from django.views import generic
from django.forms import ModelForm
from django.utils.timezone import now


@atomic
def create_cv(view: generic.View, form: ModelForm) -> models.CV: 
    """ Applicant creates CV """
    form.save(commit = False)
    cv: models.CV = form.instance
    cv.applicant = view.request.user
    cv.save()
    return cv


@atomic
def update_cv(view: generic.View, form: ModelForm) -> models.CV:
    """ Applicant updates CV """
    form.save(commit=False)
    cv: models.CV = form.instance
    new_file: FieldFile = cv.cv_file
    cv_before_change = models.CV.objects.get(id=cv.id) # type: ignore
    old_file: FieldFile = cv_before_change.cv_file
    if old_file != new_file and old_file:
        old_file.delete()
    cv.save()
    return cv

@atomic
def archive_cv(view: generic.View, form: ModelForm) -> models.CV:
    """ Applicant archives cv """
    cv = form.instance
    cv.status = enums.CVStatuses.ARCHIVED
    cv.applications.update(
        status=enums.ApplicationStatuses.ARCHIVED,
        updated_by=view.request.user,
        updated_at=now(),
    )
    cv.save()
    return form.instance


@atomic
def submit_application(view: generic.View, form: ModelForm) -> models.Application:
    """ Applicant submits application """
    form.save(commit=False)
    application = form.instance
    application.applicant = view.request.user
    application.vacancy_id = view.request.POST.get('vacancy_id')
    application.save()
    return application

@atomic
def accept_application(view: generic.View, form: ModelForm) -> models.Application:
    """ Employer accepting application """
    form.save(commit=False)
    appl = form.instance
    appl.state = enums.ApplicationStates.ACCEPTED
    appl.save()
    return appl


@atomic
def reject_application(view: generic.View, form: ModelForm) -> models.Application:
    """ Employer rejecting application """
    form.save(commit=False)
    appl = form.instance
    appl.state = enums.ApplicationStates.REJECTED
    appl.save()
    return appl


@atomic
def register_legal_entity(view: generic.View, form: ModelForm) -> models.LegalEntity:
    """ Creating new legal entity """
    form.save(commit=False)
    new_legal_entity: models.LegalEntity = form.instance
    new_legal_entity.owner = view.request.user
    new_legal_entity.save()
    return new_legal_entity


@atomic
def archive_legal_entity(view: generic.View, form: ModelForm) -> models.LegalEntity:
    """ Archiving legal entity and all related things """
    form.save(commit=False)
    entity = form.instance
    entity.status = enums.LegalEntityStatuses.ARCHIVED
    entity.vacancy_set.update(
        status=enums.VacancyStatuses.ARCHIVED,
        updated_by=view.request.user,
        updated_at=now(),
    )

    entity.vacancy_set.application_set.update(
        status=enums.ApplicationStatuses.ARCHIVED,
        updated_by=view.request.user,
        updated_at=now(),
    )
    entity.save()
    return entity


