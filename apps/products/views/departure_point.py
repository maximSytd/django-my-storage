from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView

from django_filters.views import FilterView

from ..models import DeparturePoint
from ..forms import DeparturePointForm
from ..filters import DeparturePointFilter

class DeparturePointListView(LoginRequiredMixin, FilterView):
    """DeparturePoint list class-based view."""

    model = DeparturePoint
    template_name = "products/list_departure_points.html"
    context_object_name = "departure_points"
    filterset_class = DeparturePointFilter
    paginate_by = 10


class DeparturePointCreateView(LoginRequiredMixin, CreateView):
    """DeparturePoint create class-based view."""

    model = DeparturePoint
    template_name = "products/create_departure_point.html"
    form_class = DeparturePointForm
    success_url = reverse_lazy("products:list_departure_points")


class DeparturePointUpdateView(LoginRequiredMixin, UpdateView):
    model = DeparturePoint
    template_name = "products/update_departure_point.html"
    form_class = DeparturePointForm
    context_object_name = "departure_point"
    success_url = reverse_lazy("products:list_departure_points")


class DeparturePointDeleteView(LoginRequiredMixin, DeleteView):
    model = DeparturePoint
    success_url = reverse_lazy("products:list_departure_points")
