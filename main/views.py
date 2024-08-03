# views.py

import io
import qrcode
import base64
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pyotp
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def home(request):
    return render(request, "main/home.html")


def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend_path = "django.contrib.auth.backends.ModelBackend"
            login(request, user, backend=backend_path)
            return redirect("/generate_qr_code/")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})


@login_required
def generate_qr_code(request):
    user = request.user
    if not user.otp_secret_key:
        user.otp_secret_key = pyotp.random_base32()
        user.save()

    otp_uri = pyotp.totp.TOTP(user.otp_secret_key).provisioning_uri(
        user.email, issuer_name="Your App Name"
    )
    img = qrcode.make(otp_uri)

    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if request.method == "POST":
        otp = request.POST.get("otp")
        totp = pyotp.TOTP(user.otp_secret_key)
        if totp.verify(otp):
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("/home")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "registration/show_qr_code.html", {"qr_code": qr_code_base64})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Don't log the user in yet, store user ID in session
                request.session["pre_2fa_user_id"] = user.pk
                return redirect("verify_otp_login")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def verify_otp_login(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        user_id = request.session.get("pre_2fa_user_id")
        if user_id:
            user = CustomUser.objects.get(pk=user_id)
            totp = pyotp.TOTP(user.otp_secret_key)
            if totp.verify(otp):
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                del request.session["pre_2fa_user_id"]  # Remove the user ID from session
                return redirect("/home")
            else:
                messages.error(request, "Invalid OTP")
        else:
            messages.error(request, "User not found.")
    return render(request, "registration/verify_otp.html")


@login_required
def show_qr_code(request):
    user = request.user
    if not user.otp_secret_key:
        user.otp_secret_key = pyotp.random_base32()
        user.save()

    otp_uri = pyotp.totp.TOTP(user.otp_secret_key).provisioning_uri(
        user.email, issuer_name="Your App Name"
    )
    img = qrcode.make(otp_uri)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
