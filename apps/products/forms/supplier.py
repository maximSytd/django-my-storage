from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Supplier


class SupplierForm(forms.ModelForm):
    """Supplier template from."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
                "placeholder": _("Input supplier's name"),
            }
        ),
        label=_("supplier's name"),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
                "placeholder": _("Input supplier's email address"),
            }
        ),
        label=_("supplier's email address"),
        required=False,
    )
    class Meta:
        model = Supplier
        fields = (
            "name",
            "email",
        )