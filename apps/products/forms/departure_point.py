from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import DeparturePoint

class DeparturePointForm(forms.ModelForm):
    """Represent departure point creation form."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input address"),
            }
        ),
        label=_("address"),
    )

    class Meta:
        model = DeparturePoint
        fields = (
            "name",
            "address",
        )