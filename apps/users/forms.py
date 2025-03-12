from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """Custom login from."""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите логин",
            }
        ),
        label="Логин",
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "class": "form-control",
            "placeholder": "Введите ваш пароль",
            }
        ),
        label="Пароль",
        required=False,
    )
