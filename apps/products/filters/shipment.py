from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import filterset
from django.contrib.contenttypes.models import ContentType

from ..models import Shipment, Product
from apps.users.models import User

class ShipmentFilter(filterset.FilterSet):
    """Represent filter of shipments list."""

    ordered_by = filterset.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice ordered by"),
            },
        ),
        label=_("ordered by"),
        required=False,
    )

    status = filterset.ChoiceFilter(
        choices=Shipment.ShipmentStatus.choices,
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice status"),
            },
        ),
        label=_("status"),
        required=False,
    )

    product = filterset.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice product"),
            },
        ),
        label=_("product"),
        method="filter_by_product",
        required=False,
    )

    class Meta:
        model = Shipment
        fields = (
            "ordered_by",
            "status",
            "product",
        )

    def filter_by_product(self, queryset, name, value):
        """Filter shipments by product."""
        return queryset.filter(
            product_activities__content_type=ContentType.objects.get_for_model(
                Shipment,
            ),
            product_activities__product=value,
        ).distinct()