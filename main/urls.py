from django.urls import path
from . import views

urlpatterns = [
    path("sign_up/", views.sign_up, name="sign_up"),
    path("application/new/", views.application_create_view, name="application_create"),
    path("application/list/", views.application_list, name="application_list"),
    path("transaction_failed/", views.transaction_failed, name="transaction_failed"),

    path(
        "legal_entities/new/", views.legal_entities_create, name="legal_entities_create"
    ),
    path("legal_entities/list/", views.legal_entities_list, name="legal_entities_list"),
    path("legal_entities/data/", views.legal_entities_data, name="legal_entities_data"),

    path("partner/new/", views.partner_create, name="partner_create"),
    path("partner/list/", views.partner_list, name="partner_list"),

    path("income/new/", views.income_create, name="income_create"),
    path("income/list/", views.income_list, name="income_list"),

    path("outcome/new/", views.outcome_create, name="outcome_create"),
    path("outcome/list/", views.outcome_list, name="outcome_list"),
]
