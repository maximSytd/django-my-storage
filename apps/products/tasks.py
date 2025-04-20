import logging

from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives

from celery import shared_task

from apps.users.models import User
from .models import Product


logger = logging.getLogger("my-storage.custom")


@shared_task(name="send_products_notifications")
def send_products_notifications() -> None:
    products_to_notify = Product.objects.with_quantity().filter(
        to_notify=True,
        is_in_shortage=True,
    )
    message = _(
    """Some products are out of stock \nA new batch should be ordered """
    "to replenish the goods. \n"
    )
    subject = _("Products out of stock")
    for product in products_to_notify:
        message += (
            f"\n{product.name}: "
            f"{product.in_storage_quantity + product.processing_quantity} / "
            f"{product.min_quantity}"
        )
    email_messages = EmailMultiAlternatives(
        subject,
        message,
        to=User.objects.filter(is_staff=True).values_list("email", flat=True),
    )
    try:
        email_messages.send()
    except Exception:
        logging.exception(
            _("Filed to send products out of stock notifications for users"),
        )