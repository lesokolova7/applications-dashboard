import datetime

from django.core.exceptions import ValidationError
from django.db import models


def validate_customer_is_not_executor(partner):
    if partner.is_executor:
        raise ValidationError(f"The selected partner {partner.name} is an executor and cannot be a customer.")


def validate_customer_is_executor(partner):
    if not partner.is_executor:
        raise ValidationError(f"The selected partner {partner.name} is an executor and cannot be a customer.")


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    referral_percentage = models.FloatField(null=False, max_length=10)
    is_executor = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


class LegalEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    partner_id = models.ForeignKey("Partner", on_delete=models.CASCADE, null=False)
    tax_number = models.CharField(max_length=255, null=False)
    legal_entity_percentage = models.FloatField(null=False, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)


class Application(models.Model):
    STATUSES = [('running', 'Running'), ('awaiting', 'Awaiting'), ('ready', 'Ready')]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, null=False, choices=[])
    created_date = models.DateTimeField(auto_now_add=True)
    resoloving_date = models.DateTimeField(null=True)
    customer_id = models.ForeignKey("Partner", null=False)
    executor_id = models.ForeignKey("Partner", null=False)
    initial_sum = models.FloatField(null=False)
    receiver_id = models.ForeignKey("LegalEntity", null=False)
    sender_id = models.ForeignKey("LegalEntity", null=False)
    executor_commission = models.FloatField(null=False)
    giving_side = models.ForeignKey("Partner", null=False)
    commission_with_interest = models.FloatField(null=False)
    comment = models.CharField(max_length=1500, null=False)
    is_documents = models.BooleanField(default=False, null=False)


    # калькулирующиеся значения, которые мы калькулируем в момент сохранения
    sum_with_executors_commission = models.FloatField(null=False)
    uncargo_sum = models.FloatField(null=False)
    referral_procentage = models.FloatField(null=False)
    clean_income = models.FloatField(null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        validate_customer_is_executor(self.giving_side)
        validate_customer_is_not_executor(self.customer)
        validate_customer_is_executor(self.executor_id)

        # Calculate sum_with_executors_commission
        self.sum_with_executors_commission = self.initial_sum * (self.executor_commission - 100) / -100

        # Calculate uncargo_sum
        self.uncargo_sum = self.initial_sum * (self.commission_with_interest - 100) / -100

        # Calculate referral_percentage
        self.referral_percentage = self.initial_sum * self.giving_side.referral_percentage / 100

        # Calculate clean_income
        self.clean_income = self.sum_with_executors_commission - self.uncargo_sum - self.referral_percentage

        super().save(*args, **kwargs)
