from .models import Reservation
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

    def clean(self):
        cleaned_data = super().clean()
        start_hour = cleaned_data.get("start_hour")
        end_hour = cleaned_data.get("end_hour")
        if start_hour and end_hour and end_hour <= start_hour:
            self.add_error(
                "end_hour", "La hora de fin debe ser posterior a la hora de inicio."
            )
        return cleaned_data

    class Meta:
        model = Reservation
        fields = ["date", "start_hour", "end_hour", "description"]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-input"}),
        }
