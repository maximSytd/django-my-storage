from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from apps.core.models import BaseModel
from ..querysets import WriteOffQuerySet
from .product_activity import ProductActivity

class WriteOff(BaseModel):
    """Represent Write off in db."""

    departure_point = models.ForeignKey(
        to="products.DeparturePoint",
        related_name="write_offs",
        on_delete=models.SET_NULL,
        verbose_name=_("Departure point"),
        null=True,
    )
    is_manual = models.BooleanField(
        verbose_name=_("Is manual"),
        help_text=_("Indicates the way write off created, by manager or api"),
        default=True,
    )
    objects = WriteOffQuerySet.as_manager()
    product_activities = GenericRelation(
        ProductActivity,
        related_query_name='write_off',
    )
    class Meta:
        verbose_name = _("Write off")
        verbose_name_plural = _("Write offs")

    def __str__(self) -> str:
        return f"{self.id}"
