from django.urls import path

from supervacancies.vacancies import views

app_name = "vacancies"
urlpatterns = [
    path("vacancies/", views.VacanciesView.as_view(), name="list"),
    path("vacancies/search/", views.SearchVacanciesView.as_view(), name="search"),
    path("employer/", views.EmployerCockpitView.as_view(), name="employer"),
    path("applicant/", views.ApplicantCockpitView.as_view(), name="applicant"),
    path("cv/create/", views.CreateCVView.as_view(), name="cv-create"),
    path("cv/<int:pk>/update/", views.UpdateCVView.as_view(), name="cv-update"),
    path("cv/<int:pk>/archive/", views.ArchiveCVView.as_view(), name="cv-archive"),
    path("cv/<int:pk/detail/", views.DetailCVView.as_view(), name="cv-detail"),
    path("vacancy/create/", views.CreateVacancyView.as_view(), name="vacancy-create"),
    path(
        "vacancy/<int:pk>/update/",
        views.UpdateVacancyView.as_view(),
        name="vacancy-update",
    ),
    path("vacancy/<int:pk>/", views.DetailVacancyView.as_view(), name="vacancy-detail"),
    path(
        "vacancy/<int:pk>/archive/",
        views.ArchiveVacancyView.as_view(),
        name="vacancy-archive",
    ),
    path(
        "company/register/",
        views.RegisterLegalEntityView.as_view(),
        name="company-register",
    ),
    path(
        "company/<int:pk>/update/",
        views.UpdateLegalEntityView.as_view(),
        name="company-update",
    ),
    path(
        "company/<int:pk>/archive/",
        views.ArchiveLegalEntityView.as_view(),
        name="company-archive",
    ),
    path(
        "company/<int:pk>/",
        views.DetailLegalEntityView.as_view(),
        name="company-detail",
    ),
    path(
        "vacancy/<int:vacancy_id>/submit-application/",
        views.SubmitApplicationView.as_view(),
        name="application-submit",
    ),
    path(
        "application/<int:pk>/accept/",
        views.AcceptApplicationView.as_view(),
        name="application-accept",
    ),
    path(
        "application/<int:pk>/reject/",
        views.RejectApplicationView.as_view(),
        name="application-reject",
    ),
]
