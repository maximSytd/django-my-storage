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
from django.contrib.contenttypes.models import ContentType

from .. import models


class ShipmentQuerySet(QuerySet):

    def with_contents(self) -> typing.Self:
        shipment_content_type = ContentType.objects.get_for_model(models.Shipment)

        queryset = self.prefetch_related("ordered_by").annotate(
            positions_count=Count(
                'product_activities',
                distinct=True,
            )
        )

        # Префетчим все ProductActivity, связанные с Shipment
        queryset = queryset.prefetch_related(
            Prefetch(
                'product_activities',
                queryset=models.ProductActivity.objects.filter(
                    content_type=shipment_content_type,
                ),
                to_attr='all_contents',
            ),
        )

        quantity_subquery = models.ProductActivity.objects.filter(
            content_type=shipment_content_type,
            object_id=OuterRef("pk"),
        ).values(
            "object_id",
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