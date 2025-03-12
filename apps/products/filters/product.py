from django import forms
from django.utils.translation import gettext_lazy as _

from django_filters import filterset

from ..models import Product, Category


class ProductFilter(filterset.FilterSet):
    """Represent filter of products list."""

    id = filterset.NumberFilter(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "input id",
            }
        ),
        lookup_expr="iexact",
        label="id",
    )

    name = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
    )
    sku = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input sku"),
            }
        ),
        label=_("sku"),
    )
    category = filterset.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice category"),
            },
        ),
        label=_("category"),
        required=False,
    )


    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "category",
        )