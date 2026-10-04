from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

from .models import User


class RegisterForm(UserCreationForm):
    """
    Form used for citizen registration.
    """

    email = forms.EmailField(
        required=True,
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
    )

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(
            email=email
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email


class LoginForm(AuthenticationForm):
    """
    Login form.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )


class ProfileForm(forms.ModelForm):
    """
    Form used by users to update their profile.
    """

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )