from django import forms
from django.utils.translation import gettext_lazy as _

from django_filters import filterset

from ..models import Product, Category, Supplier


class ProductFilter(filterset.FilterSet):
    """Represent filter of products list."""
    name = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
        lookup_expr="icontains",
    )
    sku = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input sku"),
            }
        ),
        label=_("sku"),
        lookup_expr="icontains",
    )
    category = filterset.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select mw-25",
                "data-placeholder": _("Choice category"),
            },
        ),
        label=_("category"),
        required=False,
    )
    supplier = filterset.ModelChoiceFilter(
        queryset=Supplier.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select mw-25",
                "data-placeholder": _("Choice supplier"),
            },
        ),
        label=_("supplier"),
        required=False,
    )


    class Meta:
        model = Product
        fields = (
            "name",
            "sku",
            "category",
            "supplier",
        )