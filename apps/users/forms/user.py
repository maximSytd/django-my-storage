from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import User


class UserUpdateForm(forms.ModelForm):
    """User update form."""

    first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
                "placeholder": _("Input first name "),
            },
        ),
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-50",
                "placeholder": _("Input last name "),
            },
        ),
        required=False,
    )
    avatar = forms.ImageField(
        label=_("Input last name"),
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial_first_name = self.instance.first_name
            self.initial_last_name = self.instance.last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.cleaned_data['first_name']:
            user.first_name = self.initial_first_name
        if not self.cleaned_data['last_name']:
            user.last_name = self.initial_last_name
        if 'avatar' in self.changed_data:
            user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )
