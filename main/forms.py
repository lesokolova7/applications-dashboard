from django import forms
from .models import Application, LegalEntity, Partner
import logging

logger = logging.getLogger('django')

inputClass = "block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
checkboxClass = "!max-w-[50px] !max-h-[50px] !w-auto block rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)


class PartnerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class LegalEntitiesForm(forms.ModelForm):
    partner_id = PartnerModelChoiceField(
        queryset=Partner.objects.all(),
        label="Partner",
        widget=forms.Select(attrs={'class': inputClass})
    )

    class Meta:
        model = LegalEntity
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': inputClass, 'placeholder': 'Введите имя'}),
            "tax_number": forms.TextInput(attrs={'class': inputClass, 'placeholder': 'Введите ИНН'}),
            "legal_entity_percentage": forms.NumberInput(attrs={'class': inputClass, 'placeholder': 'Введите %'}),
        }

    def __init__(self, *args, **kwargs):
        super(LegalEntitiesForm, self).__init__(*args, **kwargs)
    #     self.fields['partner_id'] = forms.ModelChoiceField(
    #         queryset=Partner.objects.all(),
    #         widget=forms.Select(attrs={'class': 'form-control'}),
    #         label_from_instance=lambda obj: obj.name  # This will display the partner's name in the select field
    #     )


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'
        labels = {
            "name": "Имя",
            "is_executor": "Исполнитель?",
            "referral_percentage": "Реф. %",
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': inputClass, 'placeholder': 'Введите имя'}),
            "is_executor": forms.CheckboxInput(attrs={'class': checkboxClass}),
            "referral_percentage": forms.NumberInput(attrs={'class': inputClass, 'placeholder': 'Введите %'}),
        }

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "status",
            "customer_id",
            "executor_id",
            "initial_sum",
            "receiver_id",
            "sender_id",
            "executor_commission",
            "giving_side",
            "commission_with_interest",
            "comment",
            "is_documents",
        ]
