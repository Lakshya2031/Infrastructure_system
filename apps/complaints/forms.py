from django import forms

from .models import Category, Complaint, Location


class ComplaintForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Enter the location/address of the issue",
            }
        ),
    )

    latitude = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.000001",
                "placeholder": "Example: 30.3568",
            }
        ),
    )

    longitude = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.000001",
                "placeholder": "Example: 76.3647",
            }
        ),
    )

    class Meta:
        model = Complaint

        fields = [
            "category",
            "description",
            "media",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Describe the infrastructure problem..."
                    ),
                }
            ),
            "media": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_category(self):
        category = self.cleaned_data.get("category")

        if not category:
            raise forms.ValidationError(
                "Please select a category."
            )

        return category