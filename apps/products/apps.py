from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsAppConfig(AppConfig):
    """Default configuration for Products app."""

    name = "apps.products"
    verbose_name = _("Products")