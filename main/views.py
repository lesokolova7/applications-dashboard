from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect

from .forms import ApplicationForm


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


def create_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success_url")
    else:
        form = ApplicationForm()

    return render(request, "application_form.html", {"form": form})
