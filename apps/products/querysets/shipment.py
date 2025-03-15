import typing

from django.db.models import (
    Prefetch,
    Sum,
    Count,
    QuerySet,
    OuterRef,
    Subquery,
    IntegerField,
)
from django.db.models.functions import Coalesce

from .. import models

class ShipmentQueryset(QuerySet):

    def with_contains(self) -> typing.Self:
        queryset = self.prefetch_related("ordered_by").annotate(
            positions_count=Count('shipment_contents', distinct=True)
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                'shipment_contents',
                queryset=models.ShipmentContents.objects.all(),
                to_attr='all_products',
            ),
        )
        quantity_subquery = models.ShipmentContents.objects.filter(
            shipment=OuterRef("pk"),
        ).values(
            "shipment",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]
        return queryset.annotate(
            total_products_quantity=Coalesce(
                Subquery(quantity_subquery),
                0,
                output_field=IntegerField(),
            ),
        )