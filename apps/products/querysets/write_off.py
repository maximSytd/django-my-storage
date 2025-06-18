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


class WriteOffQuerySet(QuerySet):

    def with_contents(self) -> typing.Self:
        # Получаем ContentType для модели WriteOff
        writeoff_content_type = ContentType.objects.get_for_model(models.WriteOff)

        # Аннотируем количество позиций (ProductActivity, связанных с WriteOff)
        queryset = self.annotate(
            positions_count=Count(
                'product_activities',  # Используем related_name из GenericRelation
                distinct=True,
            )
        )

        # Префетчим все ProductActivity, связанные с WriteOff
        queryset = queryset.prefetch_related(
            Prefetch(
                'product_activities',  # Используем related_name из GenericRelation
                queryset=models.ProductActivity.objects.filter(
                    content_type=writeoff_content_type,
                ),
                to_attr='all_contents',
            ),
        )

        # Подзапрос для подсчета общего количества товаров в WriteOff
        quantity_subquery = models.ProductActivity.objects.filter(
            content_type=writeoff_content_type,
            object_id=OuterRef("pk"),  # Связь через object_id
        ).values(
            "object_id",  # Группируем по object_id (ID WriteOff)
        ).annotate(
            total=Sum("quantity"),
        ).values("total")[:1]

        # Аннотируем общее количество товаров
        return queryset.annotate(
            total_products_quantity=Coalesce(
                Subquery(quantity_subquery),
                0,
                output_field=IntegerField(),
            ),
        )