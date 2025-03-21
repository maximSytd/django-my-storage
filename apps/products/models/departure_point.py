from django.db import models

from django.utils.translation import gettext_lazy as _


from apps.core.models import BaseModel

class DeparturePoint(BaseModel):
    """Represent Departure point in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name")
    )
    address = models.CharField(
        max_length=240,
        verbose_name=_("Address")
    )
    #TODO: coordinates with postgis

    class Meta:
        verbose_name = _("Write off")
        verbose_name_plural = _("Write offs")

    def __str__(self) -> str:
        return f"{self.name}"
