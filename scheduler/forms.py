from .models import Proposal, Reservation
from django import forms


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        label="Día",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-input", "readonly": "readonly"}
        ),
    )
    start_hour = forms.TimeField(
        label="Hora de inicio",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
    )
    end_hour = forms.TimeField(
        label="Hora de fin",
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
    )

    class Meta:
        model = Reservation
        fields = ["date", "start_hour", "end_hour", "description"]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-input"}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["reservation", "motivation", "status"]
        widgets = {
            "status": forms.Select(choices=Proposal.STATUS),
        }
