from django import forms

from ..models import User


class UserInitialsUpdateForm(forms.ModelForm):
    """User update form."""

    first_name = forms.CharField(
        label="Введите имя",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
            },
        ),
    )
    last_name = forms.CharField(
        label="Введите фамилию",
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
            },
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )