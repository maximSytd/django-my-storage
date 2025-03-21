from django.utils.translation import gettext_lazy as _
from django import forms

from ..models import Shipment, ShipmentContents, Product
from apps.users.models import User


class ShipmentContentsForm(forms.ModelForm):
    class Meta:
        model = ShipmentContents
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


class ShipmentCreateForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['ordered_by', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents_forms = forms.formset_factory(
            ShipmentContentsForm,
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