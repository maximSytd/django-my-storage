from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import WriteOff, DeparturePoint, Product, WriteOffContents


class WriteOffContentsForm(forms.ModelForm):
    """Form for adding products to a write-off."""

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice product"),
            },
        ),
        label=_("Product"),
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Input quantity"),
            }
        ),
        label=_("Quantity"),
        min_value=1,
    )

    class Meta:
        model = WriteOffContents
        fields = ['product', 'quantity']


class WriteOffForm(forms.ModelForm):
    """Represent write off creation form."""

    departure_point = forms.ModelChoiceField(
        queryset=DeparturePoint.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice departure point where product send"),
            },
        ),
        label=_("Departure point"),
    )

    class Meta:
        model = WriteOff
        fields = ["departure_point"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents_formset = forms.formset_factory(
            WriteOffContentsForm,
            extra=1,
            can_delete=True,
        )