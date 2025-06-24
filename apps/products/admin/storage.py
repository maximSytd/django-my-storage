from django.contrib import admin

from apps.core.admin import BaseAdmin
from ..models import Storage

@admin.register(Storage)
class StorageAdmin(BaseAdmin):
    """UI for Storage model."""

    ordering = ("name",)
    list_display = (
        "name",
        "coordinates",
    )
    list_display_links = ("name",)
    search_fields = ("name",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "coordinates",
            ),
        }),
    )