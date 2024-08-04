from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApplicationForm
from .models import Application


def home(request):
    return render(request, "main/home.html")


def sign_up(request):
    """
    Creating a new user
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = UserCreationForm()

    return render(request, "registration/sign_up.html", {"form": form})


def application_create_view(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            form.update_calculated_fields()
            try:
                application.save()
                return redirect("transaction_success")
            except Exception as e:
                return redirect("transaction_failed")
    else:
        form = ApplicationForm()
    return render(request, "main/application_form.html", {"form": form})


def application_update_view(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            form.update_calculated_fields()
            try:
                application.save()
                return redirect("transaction_success")
            except Exception as e:
                return redirect("transaction_failed")
    else:
        form = ApplicationForm(instance=application)
    return render(request, "main/application_form.html", {"form": form})


def transaction_success(request):
    return render(request, "main/transaction_success.html")


def transaction_failed(request):
    return render(request, "main/transaction_failed.html")
