from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.core.models import BaseModel
from .. import querysets

class Shipment(BaseModel):
    """Represent Shipment in db."""

    ordered_by = models.ForeignKey(
        to="users.User",
        related_name="shipments",
        on_delete=models.RESTRICT,
        verbose_name=_("Ordered_by"),
    )
    class ShipmentStatus(models.TextChoices):
        IN_ASSEMBLY = "In assembly", _("In assembly")
        IN_DELIVERY = "In delivery", _("In delivery")
        BEING_UNLOADED = "Being unloaded", _("Being unloaded")
        UNDER_REVIEW = "Under review", _("Under review")
        ACCEPTED = "Accepted", _("Accepted")

    status = models.CharField(
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.IN_ASSEMBLY.value,
        verbose_name=_("Status"),
        max_length=16,
    )

    objects = querysets.ShipmentQueryset.as_manager()

    class Meta:
        verbose_name = _("Shipment")
        verbose_name_plural = _("Shipments")

    def __str__(self) -> str:
        return f"Shipment(id={self.id})"
