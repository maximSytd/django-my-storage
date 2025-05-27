from django.contrib import admin

from apps.core.admin import BaseAdmin
from ..models import DeparturePoint

@admin.register(DeparturePoint)
class DeparturePointAdmin(BaseAdmin):
    """UI for DeparturePoint model."""

    ordering = ("name",)
    list_display = (
        "name",
        "type",
        "coordinates",
    )
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("type",)
    list_editable = ("type",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "type",
                "coordinates",
            ),
        }),
    )