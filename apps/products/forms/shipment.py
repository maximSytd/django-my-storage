from django import forms
from ..models import Shipment, ShipmentContents, Product


class ShipmentContentsForm(forms.ModelForm):
    class Meta:
        model = ShipmentContents
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


class ShipmentForm(forms.ModelForm):
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