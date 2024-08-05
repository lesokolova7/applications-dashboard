from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    ExampleSecretView,
    HomeView,
    RegistrationCompleteView,
    RegistrationView,
)


app_name = "account"


urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "secret/",
        ExampleSecretView.as_view(),
        name="secret",
    ),
    path(
        "register/",
        RegistrationView.as_view(),
        name="registration",
    ),
    path(
        "register/done/",
        RegistrationCompleteView.as_view(),
        name="registration_complete",
    ),
]
