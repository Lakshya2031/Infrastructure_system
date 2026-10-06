from django import forms

from .models import Inspection


class InspectionForm(forms.ModelForm):

    class Meta:
        model = Inspection

        fields = [
            "result",
            "remarks",
            "evidence",
        ]

        widgets = {
            "result": forms.RadioSelect(),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Enter your inspection findings..."
                    ),
                }
            ),

            "evidence": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }