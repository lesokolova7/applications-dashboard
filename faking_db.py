import os
import random
import sys
import uuid
from random import choice, randint
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AcctSystem.settings")
django.setup()

from faker import Faker

from main.models import (
    Partner,
    LegalEntity,
    Income,
    Outcome,
    Application,
    ApplicationChoices,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker("ru_RU")


def create_partners(entries_num: int):
    Partner.objects.bulk_create(
        [
            Partner(
                id=uuid.uuid4(),
                name=fake.company(),
                referral_percentage=randint(0, 100),
                is_executor=fake.boolean(),
            )
            for _ in range(entries_num)
        ]
    )


def create_legal_entities(entries_num: int):
    partners = list(Partner.objects.all())
    LegalEntity.objects.bulk_create(
        [
            LegalEntity(
                id=uuid.uuid4(),
                name=fake.company(),
                partner=choice(partners),
                tax_number=fake.ssn(),
                legal_entity_percentage=randint(0, 100),
            )
            for _ in range(entries_num)
        ]
    )


def create_incomes(entries_num: int):
    partners = list(Partner.objects.filter(is_executor=True))
    Income.objects.bulk_create(
        [
            Income(
                id=uuid.uuid4(),
                executor=choice(partners),
                amount=randint(0, 100))
            for _ in range(entries_num)
        ]
    )


def create_outcomes(entries_num: int):
    partners = list(Partner.objects.filter(is_executor=False))
    Outcome.objects.bulk_create(
        [
            Outcome(
                id=uuid.uuid4(),
                customer=choice(partners),
                amount=randint(500, 10000))
            for _ in range(entries_num)
        ]
    )


def create_applications(entries_num: int):
    partners = list(Partner.objects.all())
    legal_entities = list(LegalEntity.objects.all())

    Application.objects.bulk_create(
        [
            Application(
                id=uuid.uuid4(),
                status=choice(["Ожидает", "Частичная отгрузка", "Готова"]),
                customer=random.choice([_ for _ in partners if not _.is_executor]),
                executor=random.choice([_ for _ in partners if _.is_executor]),
                initial_sum=randint(5000, 15000),
                receiver=random.choice(legal_entities),
                sender=random.choice(legal_entities),
                executor_commission=0,
                giving_side=random.choice([_ for _ in partners if _.is_executor]),
                commission_with_interest=randint(500, 2000),
                sum_with_executors_commission=0,
                uncargo_sum=0,
                referral_percentage=0,
                clean_income=0,
                comment=fake.text(max_nb_chars=200),
                is_documents=fake.boolean(),
            )
            for _ in range(entries_num)
        ]
    )


def update_applications():
    for application in Application.objects.all():
        application.executor_commission = application.executor.referral_percentage

        sum_with_executors_commission = (
            application.initial_sum * (application.executor_commission - 100) / -100
        )
        uncargo_sum = (
            application.initial_sum * (application.commission_with_interest - 100) / -100
        )
        referral_percentage = (
                application.initial_sum * (application.executor_commission / 100)
        )

        clean_income = (
                sum_with_executors_commission - uncargo_sum - referral_percentage
        )

        application.sum_with_executors_commission = round(sum_with_executors_commission, 2)
        application.uncargo_sum = round(uncargo_sum, 2)
        application.referral_percentage = round(referral_percentage, 2)
        application.clean_income = round(clean_income, 2)
        application.save()


if __name__ == "__main__":
    create_partners(25)
    create_legal_entities(25)
    create_incomes(25)
    create_outcomes(25)
    create_applications(25)
    update_applications()
