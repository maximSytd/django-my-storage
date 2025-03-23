from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import ProductActivity
from ..forms import ProductActivityForm


class ProductActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductActivity
    form_class = ProductActivityForm
    template_name = "products/update_product_activity.html"
    context_object_name = "shipment_content"
    success_url = reverse_lazy("products:list_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_page'] = self.request.META.get('HTTP_REFERER', '/')
        return context


class ProductActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductActivity
    form_class = ProductActivityForm
    success_url = reverse_lazy("products:list_products")
