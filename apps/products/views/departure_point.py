from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import DeparturePoint
from ..forms import DeparturePointForm

# class WriteOffListView(LoginRequiredMixin, ListView):
#     """WriteOff list class-based view."""

#     model = WriteOff
#     template_name = "products/list_write_offs.html"
#     context_object_name = "write_offs"


class DeparturePointCreateView(LoginRequiredMixin, CreateView):
    """DeparturePoint create class-based view."""

    model = DeparturePoint
    template_name = "products/create_departure_point.html"
    form_class = DeparturePointForm
    success_url = reverse_lazy("products:list_write_offs")


# class SupplierUpdateView(LoginRequiredMixin, UpdateView):
#     model = Supplier
#     template_name = "products/update_supplier.html"
#     form_class = SupplierForm
#     success_url = reverse_lazy("products:list_suppliers")
