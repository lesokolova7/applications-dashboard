from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date

from .forms import ApplicationForm, LegalEntitiesForm, PartnerForm, IncomeForm, OutcomeForm, ApplicationFilterForm, \
    IncomeFilterForm
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
    filter_form = ApplicationFilterForm(request.GET)

    if filter_form.is_valid():
        customer = filter_form.cleaned_data.get('customer')
        executor = filter_form.cleaned_data.get('executor')
        legal_entity = filter_form.cleaned_data.get('legal_entity')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        sort_by_sum = request.GET.get('sort_by_sum')

        if customer:
            applications = applications.filter(customer=customer)
        if executor:
            applications = applications.filter(executor=executor)
        if legal_entity:
            applications = applications.filter(
                Q(receiver=legal_entity) |
                Q(sender=legal_entity)
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
            if sort_by_sum == 'asc':
                applications = applications.order_by('initial_sum')
            elif sort_by_sum == 'desc':
                applications = applications.order_by('-initial_sum')

    if not sort_by_sum:
        applications = applications.order_by('-created_date')

    return render(request, "application/application_list.html",
                  {"applications": applications, "filter_form": filter_form})


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
    filter_form = IncomeFilterForm(request.GET)

    if filter_form.is_valid():
        executor = filter_form.cleaned_data.get('executor')
        sort_by_amount = request.GET.get('sort_by_amount')
        sort_by_created_at = request.GET.get('sort_by_created_at')

        if executor:
            incomes = incomes.filter(executor=executor)

        if sort_by_amount:
            if sort_by_amount == 'asc':
                incomes = incomes.order_by('amount')
            elif sort_by_amount == 'desc':
                incomes = incomes.order_by('-amount')

        if sort_by_created_at:
            if sort_by_created_at == 'asc':
                incomes = incomes.order_by('created_at')
            elif sort_by_created_at == 'desc':
                incomes = incomes.order_by('-created_at')

    return render(request, "income/income_list.html", {"incomes": incomes, "filter_form": filter_form})


def outcome_list(request):
    outcomes = Outcome.objects.all()
    filter_form = OutcomeForm(request.GET)

    if filter_form.is_valid():
        executor = filter_form.cleaned_data.get('customer')
        sort_by_amount = request.GET.get('sort_by_amount')
        sort_by_created_at = request.GET.get('sort_by_created_at')

        if executor:
            outcomes = outcomes.filter(executor=executor)

        if sort_by_amount:
            if sort_by_amount == 'asc':
                outcomes = outcomes.order_by('amount')
            elif sort_by_amount == 'desc':
                outcomes = outcomes.order_by('-amount')

        if sort_by_created_at:
            if sort_by_created_at == 'asc':
                outcomes = outcomes.order_by('created_at')
            elif sort_by_created_at == 'desc':
                outcomes = outcomes.order_by('-created_at')

    return render(request, "outcome/outcome_list.html", {"outcomes": outcomes, "filter_form": filter_form})


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


def partner_data(request):
    role = request.GET.get('role')

    if role == 'executor':
        partners = Partner.objects.filter(is_executor=True)
    else:
        partners = Partner.objects.filter(is_executor=False)

    partner_list_data = [{'id': partner.id, 'name': partner.name} for partner in partners]

    return JsonResponse({'partners': partner_list_data})


def discrepancy_view(request):
    partners = Partner.objects.all()
    applications = Application.objects.all()

    # # Filter applications based on request parameters
    # if request.GET.get('partner'):
    #     partner_id = request.GET.get('partner')
    #     applications = applications.filter(executor_id=partner_id)
    #
    # if request.GET.get('start_date') and request.GET.get('end_date'):
    #     start_date = parse_date(request.GET.get('start_date'))
    #     end_date = parse_date(request.GET.get('end_date'))
    #     applications = applications.filter(created_date__range=(start_date, end_date))
    #
    # income_sum = applications.aggregate(Sum('initial_sum'))['initial_sum__sum'] or 0
    # outcome_sum = Outcome.objects.filter(customer_id__in=applications.values('customer_id')).aggregate(Sum('amount'))['amount__sum'] or 0
    #
    # discrepancy = income_sum - outcome_sum
    #
    # context = {
    #     'partners': partners,
    #     'applications': applications,
    #     'income_sum': income_sum,
    #     'outcome_sum': outcome_sum,
    #     'discrepancy': discrepancy
    # }

    return render(request, 'discrepancy/discrepancy.html')
