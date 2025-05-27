from django.contrib import admin

from apps.core.admin import BaseAdmin
from ..models import ProductActivity

@admin.register(ProductActivity)
class ProductActivityAdmin(BaseAdmin):
    """UI for ProductActivity model."""

    ordering = ("-product__id",)
    list_display = (
        "id",
        "content_object",
        "product",
        "quantity",
    )
    list_display_links = ("id", "content_object")
    search_fields = (
        "product__name",
        "product__sku",
    )
    list_filter = (
        "content_type",
        "product__category",
    )
    list_select_related = ("product", "content_type")

    fieldsets = (
        (None, {
            "fields": (
                "content_type",
                "object_id",
                "product",
                "quantity",
            ),
        }),
    )