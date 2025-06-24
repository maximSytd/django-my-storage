from django.db import models

from django.contrib.gis.db import models as gis_models

from django.utils.translation import gettext_lazy as _


from apps.core.models import BaseModel

class Storage(BaseModel):
    """Represent Storage in db."""

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

    class Meta:
        verbose_name = _("Storage")
        verbose_name_plural = _("Storages")

    def __str__(self) -> str:
        return f"{self.name}"
