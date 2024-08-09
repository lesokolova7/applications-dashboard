from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    WelcomeView,
    RegistrationCompleteView,
    RegistrationView,
)


app_name = "account"


urlpatterns = [
    path(
        "welcome/",
        WelcomeView.as_view(),
        name="welcome",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
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
