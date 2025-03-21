from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


from apps.core.models import BaseModel

class WriteOffContents(BaseModel):
    """Represent write off contents in db."""

    write_off = models.ForeignKey(
        to="products.WriteOff",
        related_name="write_off_contents",
        on_delete=models.CASCADE,
        verbose_name=_("Write off"),
    )
    product = models.ForeignKey(
        to="products.Product",
        related_name="write_off_contents",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000000)],
        verbose_name=_("Quantity"),
    )

    class Meta:
        verbose_name = _("Write off contents")
        verbose_name_plural = _("Write off contents")

    def __str__(self) -> str:
        return f"{self.id}"
