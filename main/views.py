import logging

from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from two_factor.utils import default_device

from .forms import (
    ApplicationForm,
    LegalEntitiesForm,
    PartnerForm,
    IncomeForm,
    OutcomeForm,
    ApplicationFilterForm,
    IncomeFilterForm,
)
from .models import Application, LegalEntity, Partner, Income, Outcome


logger = logging.getLogger(__name__)


def otp_required(view_func):
    """Decorator which verifies that the user logged in using OTP."""

    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or (
            not request.user.is_verified() and default_device(request.user)
        ):
            return redirect("two_factor:login")
        if not request.user.is_verified():
            return redirect("two_factor:setup")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@otp_required
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


@otp_required
def application_list(request):
    applications = Application.objects.all()
    filter_form = ApplicationFilterForm(request.GET)

    if filter_form.is_valid():
        customer = filter_form.cleaned_data.get("customer")
        executor = filter_form.cleaned_data.get("executor")
        legal_entity = filter_form.cleaned_data.get("legal_entity")
        start_date = filter_form.cleaned_data.get("start_date")
        end_date = filter_form.cleaned_data.get("end_date")
        sort_by_sum = request.GET.get("sort_by_sum")

        if customer:
            applications = applications.filter(customer=customer)
        if executor:
            applications = applications.filter(executor=executor)
        if legal_entity:
            applications = applications.filter(
                Q(receiver=legal_entity) | Q(sender=legal_entity)
            )
        if start_date and end_date:
            applications = applications.filter(
                created_date__range=[start_date, end_date]
            )
        elif start_date:
            applications = applications.filter(created_date__gte=start_date)
        elif end_date:
            applications = applications.filter(created_date__lte=end_date)

        if sort_by_sum:
            if sort_by_sum == "asc":
                applications = applications.order_by("initial_sum")
            elif sort_by_sum == "desc":
                applications = applications.order_by("-initial_sum")

    if not sort_by_sum:
        applications = applications.order_by("-created_date")

    return render(
        request,
        "application/application_list.html",
        {"applications": applications, "filter_form": filter_form},
    )


@otp_required
def application_update(request, pk):
    application_entity = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application_entity)
        if form.is_valid():
            form.save()
            return redirect("application_list")
    else:
        form = ApplicationForm(instance=application_entity)
    return render(request, "application/application_form.html", {"form": form})


@otp_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk)
    application.delete()
    return redirect("application_list")


def transaction_success(request):
    return render(request, "main/transaction_success.html")


def transaction_failed(request):
    return render(request, "main/transaction_failed.html")


@otp_required
def legal_entities_list(request):
    legals = LegalEntity.objects.all()
    return render(request, "legal/legal_entities_list.html", {"legals": legals})


@otp_required
def legal_entities_create(request):
    if request.method == "POST":
        form = LegalEntitiesForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("legal_entities_list")
    else:
        form = LegalEntitiesForm()
        return render(request, "legal/legal_entities_form.html", {"form": form})


@otp_required
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


@otp_required
def legal_entities_update(request, pk):
    legal_entities_entity = get_object_or_404(LegalEntity, pk=pk)
    if request.method == "POST":
        form = LegalEntitiesForm(request.POST, instance=legal_entities_entity)
        if form.is_valid():
            form.save()
            return redirect("legal_entities_list")
    else:
        form = LegalEntitiesForm(instance=legal_entities_entity)
    return render(request, "legal/legal_entities_form.html", {"form": form})


@otp_required
def legal_entities_delete(request, pk):
    legal_entity = get_object_or_404(LegalEntity, pk=pk)
    legal_entity.delete()
    return redirect("legal_entities_list")


@otp_required
def partner_list(request):
    executors = Partner.objects.filter(is_executor=True)
    customers = Partner.objects.filter(is_executor=False)
    return render(
        request,
        "partner/partner_list.html",
        {"executors": executors, "customers": customers},
    )


@otp_required
def partner_create(request):
    if request.method == "POST":
        form = PartnerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("partner_list")
    else:
        form = PartnerForm()
        return render(request, "partner/partner_form.html", {"form": form})


@otp_required
def partner_update(request, pk):
    partner_entity = get_object_or_404(Partner, pk=pk)
    if request.method == "POST":
        form = PartnerForm(request.POST, instance=partner_entity)
        if form.is_valid():
            form.save()
            return redirect("partner_list")
    else:
        form = PartnerForm(instance=partner_entity)
    return render(request, "partner/partner_form.html", {"form": form})


@otp_required
def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    partner.delete()
    return redirect("partner_list")


@otp_required
def income_list(request):
    incomes = Income.objects.all()
    filter_form = IncomeFilterForm(request.GET)

    if filter_form.is_valid():
        executor = filter_form.cleaned_data.get("executor")
        sort_by_amount = request.GET.get("sort_by_amount")
        sort_by_created_at = request.GET.get("sort_by_created_at")

        if executor:
            incomes = incomes.filter(executor=executor)

        if sort_by_amount:
            if sort_by_amount == "asc":
                incomes = incomes.order_by("amount")
            elif sort_by_amount == "desc":
                incomes = incomes.order_by("-amount")

        if sort_by_created_at:
            if sort_by_created_at == "asc":
                incomes = incomes.order_by("created_at")
            elif sort_by_created_at == "desc":
                incomes = incomes.order_by("-created_at")

    return render(
        request,
        "income/income_list.html",
        {"incomes": incomes, "filter_form": filter_form},
    )


@otp_required
def outcome_list(request):
    outcomes = Outcome.objects.all()
    filter_form = OutcomeForm(request.GET)

    if filter_form.is_valid():
        executor = filter_form.cleaned_data.get("customer")
        sort_by_amount = request.GET.get("sort_by_amount")
        sort_by_created_at = request.GET.get("sort_by_created_at")

        if executor:
            outcomes = outcomes.filter(executor=executor)

        if sort_by_amount:
            if sort_by_amount == "asc":
                outcomes = outcomes.order_by("amount")
            elif sort_by_amount == "desc":
                outcomes = outcomes.order_by("-amount")

        if sort_by_created_at:
            if sort_by_created_at == "asc":
                outcomes = outcomes.order_by("created_at")
            elif sort_by_created_at == "desc":
                outcomes = outcomes.order_by("-created_at")

    return render(
        request,
        "outcome/outcome_list.html",
        {"outcomes": outcomes, "filter_form": filter_form},
    )


@otp_required
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm()
        return render(request, "income/income_form.html", {"form": form})


@otp_required
def outcome_create(request):
    if request.method == "POST":
        form = OutcomeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("outcome_list")
    else:
        form = OutcomeForm()
        return render(request, "outcome/outcome_form.html", {"form": form})


@otp_required
def income_update(request, pk):
    income_entity = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income_entity)
        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm(instance=income_entity)
    return render(request, "income/income_form.html", {"form": form})


@otp_required
def outcome_update(request, pk):
    outcome_entity = get_object_or_404(Outcome, pk=pk)
    if request.method == "POST":
        form = OutcomeForm(request.POST, instance=outcome_entity)
        if form.is_valid():
            form.save()
            return redirect("outcome_list")
    else:
        form = OutcomeForm(instance=outcome_entity)
    return render(request, "outcome/outcome_form.html", {"form": form})


@otp_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return redirect("income_list")


def outcome_delete(request, pk):
    outcome = get_object_or_404(Outcome, pk=pk)
    outcome.delete()
    return redirect("outcome_list")


@otp_required
def partner_data(request):
    role = request.GET.get("role")

    if role == "executor":
        partners = Partner.objects.filter(is_executor=True)
    else:
        partners = Partner.objects.filter(is_executor=False)

    partner_list_data = [
        {"id": partner.id, "name": partner.name} for partner in partners
    ]

    return JsonResponse({"partners": partner_list_data})


@otp_required
def discrepancy_view(request):
    role = request.GET.get("role", "executor")
    partners = Partner.objects.filter(is_executor=(role == "executor"))

    context = {"partners": partners}

    return render(request, "discrepancy/discrepancy.html", context)


@otp_required
def partner_data_whole(request):
    partner_id = request.GET.get("partner_id")
    role = request.GET.get("role")

    if role == "executor":
        applications = Application.objects.filter(executor_id=partner_id)
        incomes = Income.objects.filter(executor_id=partner_id)
        outcomes = Outcome.objects.filter(
            customer_id__in=applications.values("customer_id")
        )
    else:
        applications = Application.objects.filter(customer_id=partner_id)
        incomes = Income.objects.filter(
            executor_id__in=applications.values("executor_id")
        )
        outcomes = Outcome.objects.filter(customer_id=partner_id)

    total_applications = applications.count()
    total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    total_outcome = outcomes.aggregate(Sum("amount"))["amount__sum"] or 0
    discrepancy = total_income - total_outcome

    application_data = []
    for app in applications:
        application_data.append(
            {
                "created_date": app.created_date,
                "id": app.id,
                "customer": app.customer.name
                if app.customer is not None
                else "Нет заказчика",
                "executor": app.executor.name
                if app.executor is not None
                else "Нет исполнителя",
                "amount": app.uncargo_sum,
                "created_at": app.created_at,
            }
        )

    incomes_data = []
    for income in incomes:
        incomes_data.append(
            {
                "created_at": income.created_at,
                "id": income.id,
                "executor": income.executor_id,
                "name": income.executor.name,
                "amount": income.amount,
            }
        )

    outcomes_data = []
    for outcome in outcomes:
        outcomes_data.append(
            {
                "created_at": outcome.created_at,
                "id": outcome.id,
                "customer": outcome.customer_id,
                "name": outcome.customer.name,
                "amount": income.amount,
            }
        )

    data = {
        "incomes": incomes_data,
        "outcomes": outcomes_data,
        "applications": application_data,
        "total_applications": total_applications,
        "total_income": total_income,
        "total_outcome": total_outcome,
        "discrepancy": discrepancy,
    }

    return JsonResponse(data)
