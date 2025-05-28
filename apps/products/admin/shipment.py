from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from apps.core.admin import BaseAdmin
from ..models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(BaseAdmin):
    """UI for Shipment model."""

    ordering = ("-created",)
    list_display = (
        "id",
        "ordered_by",
        "status_badge",
        "product_count",
        "created",
        "modified",
        "status",
    )
    list_display_links = ("id",)
    search_fields = (
        "ordered_by__username",
        "ordered_by__email",
        "id",
    )
    list_filter = (
        "status",
        ("ordered_by", admin.RelatedOnlyFieldListFilter),
        "created",
    )
    list_select_related = ("ordered_by",)
    date_hierarchy = "created"
    actions = ["mark_as_accepted"]
    list_editable = ("status",)

    fieldsets = (
        (None, {
            "fields": (
                "ordered_by",
                "status",
                "followers",
            ),
        }),
    )

    def status_badge(self, obj):
        colors = {
            "In assembly": "blue",
            "In delivery": "orange",
            "Being unloaded": "purple",
            "Under review": "yellow",
            "Accepted": "green",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 4px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = _("Status")
    status_badge.admin_order_field = "status"

    def product_count(self, obj):
        return obj.product_activities.count()
    product_count.short_description = _("Products")

    @admin.action(description="Mark selected shipments as Accepted")
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status=Shipment.ShipmentStatus.ACCEPTED)
        self.message_user(request, f"{updated} shipments marked as Accepted")

    class Media:
        css = {
            "all": ("css/admin/shipment.css",)
        }