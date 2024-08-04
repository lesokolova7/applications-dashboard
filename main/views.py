from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApplicationForm, LegalEntitiesForm, PartnerForm, IncomeForm, OutcomeForm
from .models import Application, LegalEntity, Partner, Income, Outcome
import logging

# Set up logging
logger = logging.getLogger(__name__)


def sign_up(request):
    """
    Creating a new user
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/application/list")
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
                return redirect("application_list")
            except Exception as e:
                logger.error(f"Error saving application: {e}", exc_info=True)
                return redirect("transaction_failed")
    else:
        form = ApplicationForm()
    return render(request, "application/application_form.html", {"form": form})


def application_list(request):
    applications = Application.objects.all()
    return render(request, "application/application_list.html", {"applications": applications})


def application_update(request, pk):
    application_entity = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application_entity)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application_entity)
    return render(request, 'application/application_form.html', {'form': form})


def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    application.delete()
    return redirect('application_list')


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


def legal_entities_update(request, pk):
    legal_entities_entity = get_object_or_404(LegalEntity, pk=pk)
    if request.method == "POST":
        form = LegalEntitiesForm(request.POST, instance=legal_entities_entity)
        if form.is_valid():
            form.save()
            return redirect('legal_entities_list')
    else:
        form = LegalEntitiesForm(instance=legal_entities_entity)
    return render(request, 'legal/legal_entities_form.html', {'form': form})


def legal_entities_delete(request, pk):
    legal_entity = get_object_or_404(LegalEntity, pk=pk)
    legal_entity.delete()
    return redirect('legal_entities_list')


def partner_list(request):
    executors = Partner.objects.filter(is_executor=True)
    customers = Partner.objects.filter(is_executor=False)
    return render(request, "partner/partner_list.html", {"executors": executors, "customers": customers})


def partner_create(request):
    if request.method == "POST":
        form = PartnerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("partner_list")
    else:
        form = PartnerForm()
        return render(request, "partner/partner_form.html", {"form": form})


def partner_update(request, pk):
    partner_entity = get_object_or_404(Partner, pk=pk)
    if request.method == "POST":
        form = PartnerForm(request.POST, instance=partner_entity)
        if form.is_valid():
            form.save()
            return redirect('partner_list')
    else:
        form = PartnerForm(instance=partner_entity)
    return render(request, 'partner/partner_form.html', {'form': form})


def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    partner.delete()
    return redirect('partner_list')


def income_list(request):
    incomes = Income.objects.all()
    return render(request, "income/income_list.html", {"incomes": incomes})


def outcome_list(request):
    outcomes = Outcome.objects.all()
    return render(request, "outcome/outcome_list.html", {"outcomes": outcomes})


def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm()
        return render(request, "income/income_form.html", {"form": form})


def outcome_create(request):
    if request.method == "POST":
        form = OutcomeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("outcome_list")
    else:
        form = OutcomeForm()
        return render(request, "outcome/outcome_form.html", {"form": form})


def income_update(request, pk):
    income_entity = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income_entity)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income_entity)
    return render(request, 'income/income_form.html', {'form': form})


def outcome_update(request, pk):
    outcome_entity = get_object_or_404(Outcome, pk=pk)
    if request.method == "POST":
        form = OutcomeForm(request.POST, instance=outcome_entity)
        if form.is_valid():
            form.save()
            return redirect('outcome_list')
    else:
        form = OutcomeForm(instance=outcome_entity)
    return render(request, 'outcome/outcome_form.html', {'form': form})


def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return redirect('income_list')


def outcome_delete(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    outcome.delete()
    return redirect('outcome_list')
