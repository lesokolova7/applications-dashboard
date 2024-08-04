import datetime
from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models


def validate_customer_is_not_executor(partner):
    if partner.is_executor:
        raise ValidationError(
            f"The selected partner {partner.name} is an executor and cannot be a customer."
        )


def validate_customer_is_executor(partner):
    if not partner.is_executor:
        raise ValidationError(
            f"The selected partner {partner.name} is an executor and cannot be a customer."
        )


class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    referral_percentage = models.FloatField(null=False, max_length=10)
    is_executor = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class LegalEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    partner_id = models.ForeignKey("Partner", on_delete=models.CASCADE, null=False)
    tax_number = models.CharField(max_length=255, null=False)
    legal_entity_percentage = models.FloatField(null=False, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class ApplicationChoices(Enum):
    AWAITING = "Ожидает"
    RUNNING = "Частичная отгрузка"
    READY = "Готова"

    @classmethod
    def choices(cls):
        return tuple((c.value, c.value) for c in cls)


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(choices=ApplicationChoices.choices(), max_length=25)
    created_date = models.DateTimeField(auto_now_add=True)
    resolving_date = models.DateTimeField(null=True)
    customer_id = models.ForeignKey(
        "Partner", on_delete=models.SET_NULL, related_name="partner_customer", null=True
    )
    executor_id = models.ForeignKey(
        "Partner", on_delete=models.SET_NULL, related_name="partner_executor", null=True
    )
    initial_sum = models.FloatField(null=False)
    receiver_id = models.ForeignKey(
        "LegalEntity",
        on_delete=models.SET_NULL,
        related_name="legal_entity_receiver",
        null=True,
    )
    sender_id = models.ForeignKey(
        "LegalEntity",
        on_delete=models.SET_NULL,
        related_name="legal_entity_sender",
        null=True,
    )
    executor_commission = models.FloatField(null=False)
    sum_with_executors_commission = models.FloatField(null=False)
    giving_side = models.ForeignKey(
        "Partner",
        on_delete=models.SET_NULL,
        related_name="partner_giving_side",
        null=True,
    )
    commission_with_interest = models.FloatField(null=False)
    uncargo_sum = models.FloatField(null=False)
    referral_procentage = models.FloatField(null=False)
    clean_income = models.FloatField(null=False)
    comment = models.CharField(max_length=1500, null=False)
    is_documents = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
