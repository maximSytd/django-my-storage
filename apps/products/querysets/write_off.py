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

class WriteOffQueryset(QuerySet):

    def with_contents(self) -> typing.Self:
        queryset = self.annotate(
            positions_count=Count('write_off_contents', distinct=True)
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                'write_off_contents',
                queryset=models.WriteOffContents.objects.all(),
                to_attr='all_contents',
            ),
        )
        quantity_subquery = models.WriteOffContents.objects.filter(
            write_off=OuterRef("pk"),
        ).values(
            "write_off",
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