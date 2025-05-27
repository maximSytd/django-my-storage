from django.db import models

from django.contrib.gis.db import models as gis_models

from django.utils.translation import gettext_lazy as _


from apps.core.models import BaseModel

class DeparturePoint(BaseModel):
    """Represent Departure point in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name")
    )
    coordinates = gis_models.PointField(
        verbose_name=_("Coordinates"),
        geography=True,
        srid=4326,
        null=True,
        blank=True,
    )
    class DeparturePointType(models.TextChoices):
        NOT_SPECIFIED = "Not specified", _("Not specified")
        RETAIL_PLACE = "Retail place", _("Retail place")
        SUPPLIER_STORAGE = "Supplier storage", _("Supplier storage")
        OTHER_STORAGE = "Other storage", _("Other storage")

    type = models.CharField(
        choices=DeparturePointType.choices,
        default=DeparturePointType.NOT_SPECIFIED.value,
        verbose_name=_("Type"),
        max_length=20,
    )

    class Meta:
        verbose_name = _("Departure point")
        verbose_name_plural = _("Departure points")

    def __str__(self) -> str:
        return f"{self.name}"
