from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


from apps.core.models import BaseModel

class WriteOff(BaseModel):
    """Represent Write off in db."""

    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000000)],
        verbose_name=_("Quantity"),
    )
    product = models.ForeignKey(
        to="products.Product",
        related_name="write_offs",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    departure_point = models.ForeignKey(
        to="products.DeparturePoint",
        related_name="write_offs",
        on_delete=models.CASCADE,
        verbose_name=_("Departure point"),
    )

    class Meta:
        verbose_name = _("Write off")
        verbose_name_plural = _("Write offs")

    def __str__(self) -> str:
        return f"{self.quantity}"
