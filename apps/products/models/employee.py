from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

class Employee(BaseModel):
    """Represent Employee in db."""

    full_name = models.CharField(
        max_length=120,
        verbose_name=_("Full name"),
    )
    email = models.EmailField(
        max_length=500,
        verbose_name=_("Email"),
    )

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self) -> str:
        return f"Employee(id={self.id}, full_name={self.full_name})"
