from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, resolve_url
from django.views.generic import FormView, TemplateView


class WelcomeView(TemplateView):
    template_name = "welcome.html"


class RegistrationView(FormView):
    template_name = "registration.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return redirect("account:registration_complete")


class RegistrationCompleteView(TemplateView):
    template_name = "registration_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context
