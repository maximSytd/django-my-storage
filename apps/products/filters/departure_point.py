from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import filterset

from ..models import DeparturePoint

class DeparturePointFilter(filterset.FilterSet):
    """Represent filter of departure points list."""

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

    type = filterset.ChoiceFilter(
        choices=DeparturePoint.DeparturePointType.choices,
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice type"),
            },
        ),
        label=_("type"),
        required=False,
    )

    class Meta:
        model = DeparturePoint
        fields = (
            "name",
            "type",
        )
