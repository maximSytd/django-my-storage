from django.utils.translation import gettext_lazy as _
from django import forms

from ..models import ProductActivity, Product


class ProductActivityForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by("name"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "data-placeholder": _("Choice product"),
            },
        ),
        label=_("product"),
        required=False,
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("input quantity"),
            }
        ),
        label=_("quantity of product"),
    )

    class Meta:
        model = ProductActivity
        fields = ['product', 'quantity']
