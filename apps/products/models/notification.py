from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

class Notification(BaseModel):
    """Represent Notification in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name"),
    )
    message = models.TextField(
        null=True,
        max_length=800,
        verbose_name=_("Message"),
    )
    recipient = models.EmailField(
        verbose_name=_("Recipient"),
        help_text=_("Recipient's email on which will be sent notification"),
    )

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self) -> str:
        return f"Notification(id={self.id}, recipient={self.recipient})"
