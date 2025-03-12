import typing

from django.db.models import (
    IntegerField,
    BooleanField,
    Subquery,
    QuerySet,
    OuterRef,
    Case,
    When,
    Sum,
    F,
)
from django.db.models.functions import Coalesce

from .. import models


class ProductQueryset(QuerySet):

    def with_shipments(self) -> typing.Self:
        related_subquery = models.ShipmentContents.objects.filter(
            product=OuterRef("pk"),
        )

        accepted_quantity_subquery = related_subquery.filter(
            shipment__status=models.Shipment.ShipmentStatus.ACCEPTED,
        ).values(
            "product",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        processing_quantity_subquery = related_subquery.exclude(
            shipment__status=models.Shipment.ShipmentStatus.ACCEPTED,
        ).values(
            "product",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        return self.prefetch_related("category").annotate(
            in_storage_quantity=Coalesce(
                Subquery(accepted_quantity_subquery),
                0,
                output_field=IntegerField(),
            ),
            processing_quantity=Coalesce(
                Subquery(processing_quantity_subquery),
                0,
                output_field=IntegerField(),
            ),
            is_in_shortage=Case(
                When(
                    min_quantity__gt=(
                        F("in_storage_quantity") + F("processing_quantity"),
                    ),
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            ),
        )
