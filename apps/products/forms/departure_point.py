from django import forms
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _

from ..models import DeparturePoint

class DeparturePointForm(forms.ModelForm):
    latitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control w-25",
                "placeholder": _("Select status"),
            }
        ),
        label=_("Type"),
        choices=DeparturePoint.DeparturePointType.choices,
        required=False,
    )

    class Meta:
        model = DeparturePoint
        fields = ('name', 'latitude', 'longitude', "type")
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                    "placeholder": _("Input name "),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.coordinates:
            self.initial['latitude'] = self.instance.coordinates.y
            self.initial['longitude'] = self.instance.coordinates.x

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat and lon:
            instance.coordinates = Point(lon, lat, srid=4326)
        elif not (lat or lon):
            instance.coordinates = None

        if commit:
            instance.save()
        return instance