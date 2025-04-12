from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django_filters.views import FilterView

from ..models import Supplier
from ..forms import SupplierForm
from ..filters import SupplierFilter


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """Supplier create class-based view."""

    model = Supplier
    template_name = "products/create_supplier.html"
    form_class = SupplierForm
    success_url = reverse_lazy("products:list_suppliers")


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = "products/update_supplier.html"
    form_class = SupplierForm
    success_url = reverse_lazy("products:list_suppliers")


class SupplierListView(LoginRequiredMixin, FilterView):
    """Suppliers list class-based view."""

    model = Supplier
    template_name = "products/list_suppliers.html"
    context_object_name = "suppliers"
    filterset_class = SupplierFilter


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy("products:list_suppliers")
