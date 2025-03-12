from django.db.models import Prefetch, Count, QuerySet
import typing
from .. import models

class ShipmentQueryset(QuerySet):

    def with_contains(self) -> typing.Self:
        queryset = self.annotate(
            positions_count=Count('shipment_contents', distinct=True)
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                'shipment_contents',
                queryset=models.ShipmentContents.objects.all(),
                to_attr='all_products',
            ),
        )
        return queryset