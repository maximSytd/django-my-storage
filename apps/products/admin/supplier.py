from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from ..models import Supplier

@admin.register(Supplier)
class SupplierAdmin(BaseAdmin):
    """UI for Supplier model."""

    ordering = ("name",)
    list_display = (
        "name",
        "email",
        "product_count",
    )
    list_display_links = ("name",)
    search_fields = (
        "name",
        "email",
    )

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "email",
            ),
        }),
    )

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _("Products Count")