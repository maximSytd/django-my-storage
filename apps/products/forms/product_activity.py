from django.utils.translation import gettext_lazy as _
from django import forms

from ..models import ProductActivity, Product


class ProductActivityForm(forms.ModelForm):
    class Meta:
        model = ProductActivity
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()