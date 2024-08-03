from django import forms
from .models import Application


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
