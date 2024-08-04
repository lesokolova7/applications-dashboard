from django import forms
from .models import Application, ApplicationChoices, Partner, LegalEntity

import logging

logger = logging.getLogger("django")

inputClass = "block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
checkboxClass = "!max-w-[50px] !max-h-[50px] !w-auto block rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"


class ApplicationForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=ApplicationChoices.choices(),
        label="Статус заявки: ",
        widget=forms.Select(attrs={"class": inputClass}),
    )
    customer_id = forms.ModelChoiceField(
        queryset=Partner.objects.filter(is_executor=False),
        label="Клиент: ",
        widget=forms.Select(attrs={"class": inputClass, "id": "id_customer"}),
    )
    executor_id = forms.ModelChoiceField(
        queryset=Partner.objects.filter(is_executor=True),
        label="Исполнитель: ",
        widget=forms.Select(attrs={"class": inputClass, "id": "id_executor"}),
    )
    initial_sum = forms.FloatField(
        label="Сумма приемки: ", widget=forms.NumberInput(attrs={"class": inputClass})
    )
    sender_id = forms.ModelChoiceField(
        queryset=LegalEntity.objects.none(),
        label="Юридическое лицо клиента",
        widget=forms.Select(attrs={"class": inputClass, "id": "id_sender"}),
    )
    receiver_id = forms.ModelChoiceField(
        queryset=LegalEntity.objects.none(),
        label="Юридическое лицо исполнителя: ",
        widget=forms.Select(attrs={"class": inputClass, "id": "id_receiver"}),
    )
    executor_commission = forms.FloatField(
        label="Комиссия исполнителя: ",
        widget=forms.NumberInput(attrs={"class": inputClass}),
    )
    giving_side = forms.ModelChoiceField(
        queryset=Partner.objects.filter(is_executor=True),
        label="Выдающая сторона: ",
        widget=forms.Select(attrs={"class": inputClass}),
    )

    commission_with_interest = forms.FloatField(
        label="Комиссия с учетом нашего интереса: ",
        widget=forms.NumberInput(attrs={"class": inputClass}),
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"class": inputClass, "rows": 4}),
        label="Комментарий: ",
    )
    is_documents = forms.BooleanField(
        required=False,
        label="Документы предоставлены: ",
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    sum_with_executors_commission = forms.FloatField(
        label="Сумма с учетом комиссии исполнителя: ",
        required=False,
        widget=forms.TextInput(attrs={"class": inputClass, "readonly": "readonly"}),
    )
    uncargo_sum = forms.FloatField(
        label="Сумма отгрузки: ",
        required=False,
        widget=forms.TextInput(attrs={"class": inputClass, "readonly": "readonly"}),
    )
    referral_procentage = forms.FloatField(
        label="Реф %: ",
        required=False,
        widget=forms.TextInput(attrs={"class": inputClass, "readonly": "readonly"}),
    )
    clean_income = forms.FloatField(
        label="Чистый доход: ",
        required=False,
        widget=forms.TextInput(attrs={"class": inputClass, "readonly": "readonly"}),
    )

    class Meta:
        model = Application
        fields = [
            "status",
            "customer_id",
            "executor_id",
            "initial_sum",
            "sender_id",
            "receiver_id",
            "executor_commission",
            "giving_side",
            "commission_with_interest",
            "comment",
            "is_documents",
            "sum_with_executors_commission",
            "uncargo_sum",
            "referral_procentage",
            "clean_income",
        ]

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        if "executor_id" in self.data:
            try:
                executor_id = int(self.data.get("executor_id"))
                self.fields["receiver_id"].queryset = LegalEntity.objects.filter(
                    partner_id=executor_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["receiver_id"].queryset = LegalEntity.objects.filter(
                partner_id=self.instance.executor_id.id
            )

        if "customer_id" in self.data:
            try:
                customer_id = int(self.data.get("customer_id"))
                self.fields["sender_id"].queryset = LegalEntity.objects.filter(
                    partner_id=customer_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["sender_id"].queryset = LegalEntity.objects.filter(
                partner_id=self.instance.customer_id.id
            )

        self.update_calculated_fields()

    def update_calculated_fields(self):
        if self.instance.pk:
            self.instance = self.instance
            self.fields["sum_with_executors_commission"].initial = (
                    self.instance.initial_sum
                    * (self.instance.executor_commission - 100)
                    / -100
            )
            self.fields["uncargo_sum"].initial = (
                    self.instance.initial_sum
                    * (self.instance.commission_with_interest - 100)
                    / -100
            )
            self.fields["referral_procentage"].initial = (
                    self.instance.initial_sum
                    * (self.instance.executor_id.referral_percentage / 100)
            )
            self.fields["clean_income"].initial = (
                    self.fields["sum_with_executors_commission"].initial
                    - self.fields["uncargo_sum"].initial
                    - self.fields["referral_procentage"].initial
            )

    def clean_is_documents(self):
        is_documents = self.cleaned_data.get('is_documents')
        return bool(is_documents)

    def clean(self):
        cleaned_data = super().clean()
        initial_sum = cleaned_data.get("initial_sum")
        executor_commission = cleaned_data.get("executor_commission")
        commission_with_interest = cleaned_data.get("commission_with_interest")
        giving_side = cleaned_data.get("giving_side")

        if (
                initial_sum
                and executor_commission
                and commission_with_interest
                and giving_side
        ):
            sum_with_executors_commission = (
                    initial_sum * (executor_commission - 100) / -100
            )
            uncargo_sum = initial_sum * (commission_with_interest - 100) / -100
            referral_percentage = initial_sum * giving_side.referral_percentage / 100
            clean_income = (
                    sum_with_executors_commission - uncargo_sum - referral_percentage
            )

            cleaned_data["sum_with_executors_commission"] = (
                sum_with_executors_commission
            )
            cleaned_data["uncargo_sum"] = uncargo_sum
            cleaned_data["referral_percentage"] = referral_percentage
            cleaned_data["clean_income"] = clean_income

        return cleaned_data









































class PartnerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class LegalEntitiesForm(forms.ModelForm):
    partner_id = PartnerModelChoiceField(
        queryset=Partner.objects.all(),
        label="Partner",
        widget=forms.Select(attrs={"class": inputClass}),
    )

    class Meta:
        model = LegalEntity
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": inputClass, "placeholder": "Введите имя"}
            ),
            "tax_number": forms.TextInput(
                attrs={"class": inputClass, "placeholder": "Введите ИНН"}
            ),
            "legal_entity_percentage": forms.NumberInput(
                attrs={"class": inputClass, "placeholder": "Введите %"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(LegalEntitiesForm, self).__init__(*args, **kwargs)


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = "__all__"
        labels = {
            "name": "Имя",
            "is_executor": "Исполнитель?",
            "referral_percentage": "Реф. %",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": inputClass, "placeholder": "Введите имя"}
            ),
            "is_executor": forms.CheckboxInput(attrs={"class": checkboxClass}),
            "referral_percentage": forms.NumberInput(
                attrs={"class": inputClass, "placeholder": "Введите %"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
