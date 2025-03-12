from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

class Category(BaseModel):
    """Represent Category in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        null=True,
        max_length=500,
        verbose_name=_("Description"),
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f"{self.name}"
