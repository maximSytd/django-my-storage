from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Max, Min, Q
from django.db.models.functions import TruncMonth
from django.contrib.contenttypes.models import ContentType

from datetime import datetime
from ..models import ProductActivity, WriteOff, Shipment, Product, Supplier

class DashboardSummaryView(LoginRequiredMixin, TemplateView):

    template_name = "products/summary_dashboard.html"

class ProductActivitySummaryView(LoginRequiredMixin, TemplateView):
    """Class-based view for product activity summary page."""

    template_name = "products/summary_product_activity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем список доступных годов
        years_list = ProductActivity.objects.dates('created', 'year').values_list(
            'created__year', flat=True
        ).distinct()

        # Получаем выбранный год
        selected_year = self.request.GET.get('year', datetime.now().year)

        # Базовый QuerySet для активности
        activities = ProductActivity.objects.filter(created__year=selected_year)
        total_count = activities.count()

        # Общая статистика по количеству
        quantity_stats = activities.aggregate(
            average=Avg('quantity'),
            max=Max('quantity'),
            min=Min('quantity')
        )

        # Статистика по отгрузкам (уникальные Shipment)
        shipment_count = Shipment.objects.filter(
            product_activities__created__year=selected_year
        ).distinct().count()

        # Среднее количество товаров в отгрузках
        shipment_avg = activities.filter(
            content_type__model='shipment'
        ).aggregate(avg=Avg('quantity'))['avg']

        # Статистика по списаниям (уникальные WriteOff)
        writeoff_count = WriteOff.objects.filter(
            product_activities__created__year=selected_year
        ).distinct().count()

        # Среднее количество товаров в списаниях
        writeoff_avg = activities.filter(
            content_type__model='writeoff'
        ).aggregate(avg=Avg('quantity'))['avg']

        # Получаем типы контента для Shipment и WriteOff
        shipment_content_type = ContentType.objects.get_for_model(Shipment)
        writeoff_content_type = ContentType.objects.get_for_model(WriteOff)

        # Самый активный продукт (по участию в уникальных Shipment/WriteOff)
        most_active_product = Product.objects.filter(
            Q(product_activities__content_type=shipment_content_type) |
            Q(product_activities__content_type=writeoff_content_type),
            product_activities__created__year=selected_year
        ).annotate(
            operation_count=Count('product_activities__object_id', distinct=True)
        ).order_by('-operation_count').first()

        # Статистика по месяцам
        monthly_stat = activities.annotate(
            month=TruncMonth('created')
        ).values('month').annotate(
            count=Count('id'),
            shipment_count=Count('object_id', 
                              filter=Q(content_type=shipment_content_type), 
                              distinct=True),
            writeoff_count=Count('object_id', 
                               filter=Q(content_type=writeoff_content_type), 
                               distinct=True)
        ).order_by('month')

        # Форматируем данные для графика
        formatted_monthly_stat = [
            {
                'month': entry['month'].strftime('%B'),
                'count': entry['count'],
                'shipment_count': entry['shipment_count'],
                'writeoff_count': entry['writeoff_count']
            }
            for entry in monthly_stat
        ]

        context.update({
            'years_list': years_list,
            'selected_year': selected_year,
            'total_count': total_count,
            'most_active_product': {
                'name': most_active_product.name if most_active_product else None,
                'count': most_active_product.operation_count if most_active_product else 0
            },
            'average_quantity': round(quantity_stats['average'], 2) if quantity_stats['average'] else 0,
            'max_quantity': quantity_stats['max'],
            'min_quantity': quantity_stats['min'],
            'monthly_stat': formatted_monthly_stat,
            'total_operations': sum(entry['count'] for entry in formatted_monthly_stat),
            'shipment_count': shipment_count,
            'shipment_avg': int(round(shipment_avg, 0)) if shipment_avg else 0,
            'writeoff_count': writeoff_count,
            'writeoff_avg': int(round(writeoff_avg, 0)) if writeoff_avg else 0,
        })

        return context

class SupplierSummaryView(LoginRequiredMixin, ListView):
    """Supplier statistics dashboard with general and per-supplier views"""
    
    template_name = "products/summary_supplier.html"
    context_object_name = "suppliers"
    queryset = Supplier.objects.with_product_counts().order_by("-name")
