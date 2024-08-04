from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApplicationForm, LegalEntitiesForm, PartnerForm
from .models import Application, LegalEntity, Partner
import logging


# Set up logging
logger = logging.getLogger(__name__)

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
                logger.error(f"Error saving application: {e}", exc_info=True)
                return redirect("transaction_failed")
    else:
        form = ApplicationForm()
    return render(request, "application/application_form.html", {"form": form})


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
                logger.error(f"Error saving application: {e}", exc_info=True)
                return redirect("transaction_failed")
    else:
        form = ApplicationForm(instance=application)
    return render(request, "main/application_form.html", {"form": form})


def transaction_success(request):
    return render(request, "main/transaction_success.html")


def transaction_failed(request):
    return render(request, "main/transaction_failed.html")


def legal_entities_list(request):
    legals = LegalEntity.objects.all()
    return render(request, "legal/legal_entities_list.html", {"legals": legals})


def legal_entities_create(request):
    if request.method == "POST":
        form = LegalEntitiesForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("legal_entities_list")
    else:
        form = LegalEntitiesForm()
        return render(request, "legal/legal_entities_form.html", {"form": form})


def legal_entities_data(request):
    legal_entity_data = LegalEntity.objects.all()
    data = list(
        legal_entity_data.values(
            "id",
            "name",
            "partner_id",
            "tax_number",
            "legal_entity_percentage",
            "created_at",
            "updated_at",
        )
    )
    return JsonResponse(data, safe=False)


def partner_list(request):
    partners = Partner.objects.all()
    return render(request, "partner/partner_list.html", {"partners": partners})


def partner_create(request):
    if request.method == "POST":
        form = PartnerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("partner_list")
    else:
        form = PartnerForm()
        return render(request, "partner/partner_form.html", {"form": form})
