from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class UserCreationForm(UserCreationForm):
    username = UsernameField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email1 = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    email2 = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "email1", "email2", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email1"]
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("email1") != cleaned_data.get("email2"):
            raise forms.ValidationError({"email2": ["Emails do not match."]})


class AuthenticationForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, verification_code: int, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.verification_code: int = verification_code

    verification_code_email = forms.IntegerField(
        required=True,
        max_value=999999,
        min_value=100000,
        widget=forms.NumberInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("verification_code_email") != self.verification_code:
            raise forms.ValidationError(
                {
                    "verification_code_email": [
                        "Verification code doesn't match the one send via email!"
                    ]
                }
            )
