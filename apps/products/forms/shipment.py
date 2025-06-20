from django.utils.translation import gettext_lazy as _
from django import forms

from apps.users.models import User
from ..models import Shipment
from .product_activity import ProductActivity

class ShipmentCreateForm(forms.ModelForm):
    ordered_by = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        widget=forms.Select(
            attrs={
                "class": "form-control w-25 select2",
                "placeholder": _("Select status"),
            }
        ),
        label=_("Ordered by"),
        required=False,
    )
    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("Select status"),
            }
        ),
        label=_("Status"),
        choices=Shipment.ShipmentStatus.choices,
        required=False,
    )
    class Meta:
        model = Shipment
        fields = ['ordered_by', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents_forms = forms.formset_factory(
            ProductActivity,
            extra=1,
            can_delete=True,
        )

class ShipmentUpdateForm(forms.ModelForm):
    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": _("Select status"),
            }
        ),
        label=_("Status"),
        choices=Shipment.ShipmentStatus.choices,
        required=False,
    )
    class Meta:
        model = Shipment
        fields = ['status']