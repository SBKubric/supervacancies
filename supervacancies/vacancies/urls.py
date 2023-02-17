from django.urls import path
from supervacancies.vacancies import views


app_name = "vacancies"
urlpatterns = [
    path("vacancies/", views.VacanciesView.as_view(), name="list"),
    path("vacancies/search/", views.SearchVacanciesView.as_view(), name="search"),
    path("employer/", views.EmployerCockpitView.as_view(), name="employer"),
    path("applicant/", views.ApplicantCockpitView.as_view(), name="applicant"),
    path("cv/create/", views.CreateCVView.as_view(), name="cv-create"),
    path(
        "cv/update/<int:pk>/", 
        views.UpdateCVView.as_view(), 
        name="cv-update"
    ),
    path(
        "cv/archive/<int:pk>/", 
        views.ArchiveCVView.as_view(), 
        name="cv-archive"
    ),
    path("vacancy/create/", views.CreateVacancyView.as_view(), name="vacancy-create"),
    path(
        "vacancy/update/<int:pk>/", 
        views.UpdateVacancyView.as_view(), 
        name="vacancy-update"
    ),
    path(
        "vacancy/archive/<int:pk>/", 
        views.ArchiveVacancyView.as_view(), 
        name="vacancy-archive"
    ),
    path("company/register/", views.RegisterLegalEntityView.as_view(), name="company-register"),
    path(
        "company/update/<int:pk>/", 
        views.UpdateLegalEntityView.as_view(), 
        name="company-update"
    ),
    path(
        "company/archive/<int:pk>/", 
        views.ArchiveLegalEntityView.as_view(), 
        name="company-archive"
    ),
    path("application/submit/", views.SubmitApplicationView.as_view(), name="application-submit"),
    path(
        "application/accept/<int:pk>/", 
        views.AcceptApplicationView.as_view(), 
        name="application-accept"
    ),
    path(
        "application/reject/<int:pk>/", 
        views.RejectApplicationView.as_view(), 
        name="application-reject"
    ),
]

