from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect


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
