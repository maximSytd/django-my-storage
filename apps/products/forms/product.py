from django import forms
from django.utils.translation import gettext_lazy as _

from django_measurement.forms import MeasurementField, MeasurementWidget
from measurement.measures import Weight

from ..models import Product, Category, Supplier
from ..validators import validate_image_size

class ProductForm(forms.ModelForm):
    """Represent product creation form."""

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("input name"),
            }
        ),
        label=_("name"),
    )
    sku = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("input sku"),
            }
        ),
        label=_("sku"),
    )
    weight = MeasurementField(
        measurement=Weight,
        widget=MeasurementWidget(
            unit_choices=(
                ("kg", _("Kilograms")),
            ),
            attrs={
                'class': 'form-control w-25',
                'placeholder': _('Input weight'),
                'step': '0.001',
                'min': '0',
                'max': '100000',
            }
        ),
        min_value=Weight(g=1),
        max_value=Weight(kg=1000),
        label=_("weight of 1 item in packaging"),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select w-50",
                "data-placeholder": _("Choice category"),
            },
        ),
        label=_("category"),
        required=False,
    )
    min_quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("input min quantity"),
            }
        ),
        label=_("minimal quantity of product in storage"),
    )
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "w-50",
                'accept': 'image/*',
            },
        ),
        allow_empty_file=False,
        validators=[validate_image_size],
        required=False,
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "select2 form-select w-25",
                "data-placeholder": _("Choice supplier"),
            },
        ),
        label=_("supplier"),
    )
    to_notify = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check me-2",
            },
        ),
        label=_("notify manager via email when product is in shortage"),
        required=False,
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "sku",
            "weight",
            "category",
            "min_quantity",
            "picture",
            "supplier",
            "to_notify",
        )