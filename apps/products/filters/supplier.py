from django import forms
from django.utils.translation import gettext_lazy as _

from django_filters import filterset

from ..models import Product, Supplier


class SupplierFilter(filterset.FilterSet):
    """Represent filter of suppliers list."""

    name = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
        required=False,
        lookup_expr="icontains",
    )
    email = filterset.CharFilter(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input email"),
            }
        ),
        label=_("email"),
        required=False,
        lookup_expr="icontains",
    )

    def filter_product(queryset, name, value):
        return queryset.filter(products=value)

    product = filterset.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select mw-25",
                "data-placeholder": _("Choice Product"),
            },
        ),
        label=_("supplier"),
        required=False,
        method=filter_product,
    )


    class Meta:
        model = Supplier
        fields = (
            "name",
            "email",
            "product",
        )