from .models import LegalEntity
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from .forms import ApplicationForm, LegalEntitiesForm


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


def legal_entities_list(request):
    legals = LegalEntity.objects.all()
    return render(request, 'legal/legal_entities_list.html', {'legals': legals})


def legal_entities_create(request):
    if request.method == "POST":
        form = LegalEntitiesForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('legal/legal_entities_list')
    else:
        form = LegalEntitiesForm()
        return render(request, 'legal/legal_entities_form.html', {'form': form})
