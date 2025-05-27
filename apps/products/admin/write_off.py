from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from ..models import WriteOff

@admin.register(WriteOff)
class WriteOffAdmin(BaseAdmin):
    """UI for WriteOff model."""

    ordering = ("-created",)
    list_display = (
        "id",
        "departure_point",
        "is_manual",
        "product_count",
    )
    list_display_links = ("id",)
    search_fields = (
        "departure_point__name",
        "id",
    )
    list_filter = (
        "is_manual",
        "departure_point",
    )
    list_select_related = ("departure_point",)

    fieldsets = (
        (None, {
            "fields": (
                "departure_point",
                "is_manual",
            ),
        }),
    )

    def product_count(self, obj):
        return obj.product_activities.count()
    product_count.short_description = _("Products Count")