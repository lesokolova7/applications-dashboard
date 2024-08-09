from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("application/new/", views.application_create_view, name="application_create"),
    path("application/<uuid:pk>/", views.application_update, name="application_update"),
    path("application/list/", views.application_list, name="application_list"),
    path(
        "application/<uuid:pk>/delete/",
        views.application_delete,
        name="application_delete",
    ),
    path("transaction_failed/", views.transaction_failed, name="transaction_failed"),
    path(
        "legal_entities/new/", views.legal_entities_create, name="legal_entities_create"
    ),
    path("legal_entities/list/", views.legal_entities_list, name="legal_entities_list"),
    path("legal_entities/data/", views.legal_entities_data, name="legal_entities_data"),
    path(
        "legal_entities/<uuid:pk>/",
        views.legal_entities_update,
        name="legal_entities_update",
    ),
    path(
        "legal_entities/<uuid:pk>/delete/",
        views.legal_entities_delete,
        name="legal_entities_delete",
    ),
    path("partner/new/", views.partner_create, name="partner_create"),
    path("partner/list/", views.partner_list, name="partner_list"),
    path("partner/<uuid:pk>/", views.partner_update, name="partner_update"),
    path("partner/<uuid:pk>/delete/", views.partner_delete, name="partner_delete"),
    path("partner/data/", views.partner_data, name="partner_data"),
    path("partner/data/all", views.partner_data_whole, name="partner_data_whole"),
    path("income/new/", views.income_create, name="income_create"),
    path("income/list/", views.income_list, name="income_list"),
    path("income/<uuid:pk>/", views.income_update, name="income_update"),
    path("income/<uuid:pk>/delete/", views.income_delete, name="income_delete"),
    path("outcome/new/", views.outcome_create, name="outcome_create"),
    path("outcome/list/", views.outcome_list, name="outcome_list"),
    path("outcome/<uuid:pk>/", views.outcome_update, name="outcome_update"),
    path("outcome/<uuid:pk>/delete/", views.outcome_delete, name="outcome_delete"),
    path("discrepancy/", views.discrepancy_view, name="discrepancy_view"),
]
