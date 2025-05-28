import logging

from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from celery import shared_task

from apps.users.models import User
from .models import Product, Shipment


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


@shared_task(name="send_shipment_status_notification")
def send_shipment_status_notification(shipment_id: int) -> None:
    shipment = (
        Shipment.objects
        .filter(id=shipment_id)
        .with_contents()
        .first()
    )
    if not shipment:
        logging.error(f"Shipment {shipment_id} not found")
        return

    subject = _("Shipment #{} Received in Warehouse").format(shipment_id)

    context = {
        'shipment': shipment,
        'subject': subject,
        "domain": Site.objects.get_current().domain,
    }
    message = _(
        """Shipment #{} has been successfully received in the warehouse.\n\n"""
        """All items have been checked and recorded in the system.\n"""
    ).format(shipment_id)
    html_message = render_to_string(
        'emails/shipment_status_notification.html',
        context,
    )

    email = EmailMultiAlternatives(
        subject,
        message,
        to=shipment.followers.values_list("email", flat=True),
    )
    email.attach_alternative(html_message, "text/html")

    email.extra_headers = {
        'Precedence': 'bulk',
        'X-Mailru-Msgtype': 'transactional',
    }
    try:
        email.send()
    except Exception:
        logging.exception("Failed to send shipment notification")