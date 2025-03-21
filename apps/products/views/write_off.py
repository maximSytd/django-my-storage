from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import WriteOff
from ..forms import WriteOffForm

class WriteOffListView(LoginRequiredMixin, ListView):
    """WriteOff list class-based view."""

    model = WriteOff
    template_name = "products/list_write_offs.html"
    context_object_name = "write_offs"


class WriteOffCreateView(LoginRequiredMixin, CreateView):
    """WriteOff create class-based view."""

    model = WriteOff
    template_name = "products/create_write_off.html"
    form_class = WriteOffForm
    success_url = reverse_lazy("products:list_write_offs")


class WriteOffUpdateView(LoginRequiredMixin, UpdateView):
    model = WriteOff
    template_name = "products/update_write_off.html"
    form_class = WriteOffForm
    success_url = reverse_lazy("products:list_write_offs")
