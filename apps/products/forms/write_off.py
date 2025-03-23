from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import WriteOff, DeparturePoint
from .product_activity import ProductActivityForm

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
            ProductActivityForm,
            extra=1,
            can_delete=True,
        )