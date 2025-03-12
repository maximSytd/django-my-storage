from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

class Supplier(BaseModel):
    """Represent Supplier in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name"),
    )
    email = models.EmailField(
        max_length=200,
        verbose_name=_("Email"),
    )

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self) -> str:
        return f"{self.name}"
