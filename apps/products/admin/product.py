from django.contrib import admin

from imagekit.admin import AdminThumbnail

from apps.core.admin import BaseAdmin
from ..models import Product


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    """UI for Product model."""

    ordering = ("name",)
    avatar_thumbnail = AdminThumbnail(image_field="picture_thumbnail")
    readonly_fields = (
    )
    list_display = (
        "avatar_thumbnail",
        "name",
        "sku",
        "category",
        "weight",
        "to_notify",
        "supplier",
    )
    list_display_links = (
        "name",
        "sku",
        "category",
        "supplier",
    )
    search_fields = (
        "name",
        "sku",
    )