from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from ..models import Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label=_("name"),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'input category name'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('name', css_class='form-control')
        )

    class Meta:
        model = Category
        fields = ["name"]