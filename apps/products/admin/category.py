from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from ..models import Category

@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """UI for Category model."""

    ordering = ("name",)
    list_display = (
        "name",
        "description_short",
        "product_count",
    )
    list_display_links = ("name",)
    search_fields = ("name",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "description",
            ),
        }),
    )

    def description_short(self, obj):
        return obj.description[:100] + "..." if obj.description else "-"
    description_short.short_description = _("Description")

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _("Total products with category")