from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Product, Category, Supplier
from ..validators import validate_image_size

class ProductForm(forms.ModelForm):
    """Represent product creation form."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
    )
    sku = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input sku"),
            }
        ),
        label=_("sku"),
    )
    category = forms.ModelChoiceField(
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
    min_quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": _("input min quantity"),
            }
        ),
        label=_("minimal quantity of product in storage"),
    )
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={'accept': 'image/*'},
        ),
        allow_empty_file=False,
        validators=[validate_image_size],
        required=False,
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select",
                "data-placeholder": _("Choice supplier"),
            },
        ),
        label=_("supplier"),
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "sku",
            "category",
            "min_quantity",
            "picture",
            "supplier",
        )