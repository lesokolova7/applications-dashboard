from django import forms
from .models import Application, LegalEntity, Partner
import logging

logger = logging.getLogger('django')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)


class LegalEntitiesForm(forms.ModelForm):
    class Meta:
        model = LegalEntity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LegalEntitiesForm, self).__init__(*args, **kwargs)


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
