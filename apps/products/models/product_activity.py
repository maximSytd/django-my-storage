from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


from apps.core.models import BaseModel

class ProductActivity(BaseModel):
    """Represent Product activity in db."""

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Object ID"),
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )
    product = models.ForeignKey(
        to="products.Product",
        related_name="product_activities",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000000)],
        verbose_name=_("Quantity"),
    )

    class Meta:
        verbose_name = _("Product activity")
        verbose_name_plural = _("Product activities")

    def __str__(self) -> str:
        return f"{self.id}"
