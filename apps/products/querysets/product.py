import typing
from django.db.models import (
    IntegerField,
    BooleanField,
    Subquery,
    QuerySet,
    OuterRef,
    Prefetch,
    Case,
    When,
    Sum,
    F,
)
from django.db.models.functions import Coalesce
from django.contrib.contenttypes.models import ContentType

from .. import models


class ProductQueryset(QuerySet):

    def with_quantity(self) -> typing.Self:
        shipment_content_type = ContentType.objects.get_for_model(models.Shipment)
        writeoff_content_type = ContentType.objects.get_for_model(models.WriteOff)

        accepted_quantity_subquery = models.ProductActivity.objects.filter(
            product=OuterRef("pk"),
            content_type=shipment_content_type,
            shipment__status=models.Shipment.ShipmentStatus.ACCEPTED,
        ).values(
            "product",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        writeoff_quantity_subquery = models.ProductActivity.objects.filter(
            product=OuterRef("pk"),
            content_type=writeoff_content_type,
        ).values(
            "product",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        processing_quantity_subquery = models.ProductActivity.objects.filter(
            product=OuterRef("pk"),
            content_type=shipment_content_type,
        ).exclude(
            shipment__status=models.Shipment.ShipmentStatus.ACCEPTED,
        ).values(
            "product",
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        return self.prefetch_related(
                Prefetch(
                'product_activities',
                    queryset=models.ProductActivity.objects.all().prefetch_related("content_type"),
                    to_attr='all_activities',
                ),
            ).prefetch_related("category").annotate(
            in_storage_quantity=Coalesce(
                Subquery(accepted_quantity_subquery),
                0,
                output_field=IntegerField(),
            ) - Coalesce(
                Subquery(writeoff_quantity_subquery),
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
                        F("in_storage_quantity") + F("processing_quantity")
                    ),
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            ),
        )