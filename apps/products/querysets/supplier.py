from django.db.models import Sum, Count, QuerySet, IntegerField, Q, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.contrib.contenttypes.models import ContentType

from .. import models

class SupplierQuerySet(QuerySet):
    def with_product_counts(self):
        """
        Аннотирует поставщиков с:
        - общим количеством товаров
        - количеством товаров на складе (из принятых поставок)
        - количеством товаров в обработке (из поставок в других статусах)
        - количеством принятых поставок
        - количеством поставок в обработке
        """
        # Получаем ContentType для Shipment
        shipment_content_type = ContentType.objects.get_for_model(models.Shipment)
        
        # Подзапрос для количества товаров на складе (принятые активности)
        stock_quantity_subquery = (
            models.ProductActivity.objects.filter(
                product__supplier=OuterRef('pk'),
                content_type=shipment_content_type,
                shipment__status=models.Shipment.ShipmentStatus.ACCEPTED
            )
            .values('product__supplier')
            .annotate(total=Sum('quantity'))
            .values('total')[:1]
        )
        
        # Подзапрос для количества товаров в обработке (не принятые активности)
        processing_quantity_subquery = (
            models.ProductActivity.objects.filter(
                product__supplier=OuterRef('pk'),
                content_type=shipment_content_type,
                shipment__status__in=[
                    models.Shipment.ShipmentStatus.IN_ASSEMBLY,
                    models.Shipment.ShipmentStatus.IN_DELIVERY,
                    models.Shipment.ShipmentStatus.BEING_UNLOADED,
                    models.Shipment.ShipmentStatus.UNDER_REVIEW
                ]
            )
            .values('product__supplier')
            .annotate(total=Sum('quantity'))
            .values('total')[:1]
        )
        
        # Подзапрос для количества принятых поставок
        accepted_shipments_subquery = (
            models.Shipment.objects.filter(
                product_activities__product__supplier=OuterRef('pk'),
                status=models.Shipment.ShipmentStatus.ACCEPTED
            )
            .values('product_activities__product__supplier')
            .annotate(count=Count('id', distinct=True))
            .values('count')[:1]
        )
        
        # Подзапрос для количества поставок в обработке
        pending_shipments_subquery = (
            models.Shipment.objects.filter(
                product_activities__product__supplier=OuterRef('pk'),
                status__in=[
                    models.Shipment.ShipmentStatus.IN_ASSEMBLY,
                    models.Shipment.ShipmentStatus.IN_DELIVERY,
                    models.Shipment.ShipmentStatus.BEING_UNLOADED,
                    models.Shipment.ShipmentStatus.UNDER_REVIEW
                ]
            )
            .values('product_activities__product__supplier')
            .annotate(count=Count('id', distinct=True))
            .values('count')[:1]
        )
        
        return self.prefetch_related("products").annotate(
            total_products=Count('products', distinct=True),
            products_stock_count=Coalesce(
                Subquery(stock_quantity_subquery),
                0,
                output_field=IntegerField()
            ),
            products_processing_count=Coalesce(
                Subquery(processing_quantity_subquery),
                0,
                output_field=IntegerField()
            ),
            accepted_shipments=Coalesce(
                Subquery(accepted_shipments_subquery),
                0,
                output_field=IntegerField()
            ),
            pending_shipments=Coalesce(
                Subquery(pending_shipments_subquery),
                0,
                output_field=IntegerField()
            )
        )