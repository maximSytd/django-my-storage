from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import WriteOff, DeparturePoint, Product

class WriteOffForm(forms.ModelForm):
    """Represent write off creation form."""

    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input quantity"),
            }
        ),
        label=_("quantity"),
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice category"),
            },
        ),
        label=_("category"),
    )
    departure_point = forms.ModelChoiceField(
        queryset=DeparturePoint.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _(
                    "Choice departure point where product send",
                ),
            },
        ),
        label=_("Departure point"),
    )

    class Meta:
        model = WriteOff
        fields = (
            "quantity",
            "product",
            "departure_point",
        )