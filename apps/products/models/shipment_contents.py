from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


from apps.core.models import BaseModel

class ShipmentContents(BaseModel):
    """Represent Shipment contents in db."""

    shipment = models.ForeignKey(
        to="products.Shipment",
        related_name="shipment_contents",
        on_delete=models.CASCADE,
        verbose_name=_("Shipment"),
    )
    product = models.ForeignKey(
        to="products.Product",
        related_name="shipments",
        on_delete=models.RESTRICT,
        verbose_name=_("Product"),
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000000)],
        verbose_name=_("Quantity"),
    )

    class Meta:
        verbose_name = _("Shipment contents")
        verbose_name_plural = _("Shipments contents")

    def __str__(self) -> str:
        return (
            f"Shipment(id={self.id}, product={self.product}, "
            f"quantity={self.quantity})"
        )
