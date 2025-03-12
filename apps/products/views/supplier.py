from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Supplier
from ..forms import SupplierForm


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



class SupplierListView(LoginRequiredMixin, ListView):
    """Suppliers list class-based view."""

    model = Supplier
    template_name = "products/list_suppliers.html"
    context_object_name = "suppliers"