from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("home/", views.home, name="home"),
    path("application/new/", views.application_create_view, name="application_create"),
    path("transaction_success/", views.transaction_success, name="transaction_success"),
    path("transaction_failed/", views.transaction_failed, name="transaction_failed"),
    path(
        "legal_entities/new/", views.legal_entities_create, name="legal_entities_create"
    ),
    path("legal_entities/list/", views.legal_entities_list, name="legal_entities_list"),
    path("legal_entities/data/", views.legal_entities_data, name="legal_entities_data"),
    path("partner/new/", views.partner_create, name="partner_create"),
    path("partner/list/", views.partner_list, name="partner_list"),
]
