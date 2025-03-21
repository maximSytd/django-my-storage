from django.views.generic import CreateView, DetailView
from django.views.generic.edit import BaseUpdateView
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django_filters.views import FilterView

from ..models import Shipment, ShipmentContents
from ..forms import (
    ShipmentCreateForm,
    ShipmentContentsForm,
    ShipmentUpdateForm,
)
from ..filters import ShipmentFilter

class ShipmentListView(LoginRequiredMixin, FilterView):
    """Shipment list class-based view."""

    model = Shipment
    filterset_class = ShipmentFilter
    template_name = "products/list_shipments.html"
    context_object_name = "shipments"
    queryset = Shipment.objects.with_contents()

class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentCreateForm
    template_name = 'products/create_shipment.html'
    success_url = reverse_lazy('products:list_shipments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['contents_formset'] = formset_factory(ShipmentContentsForm, extra=1)(self.request.POST)
        else:
            context['contents_formset'] = formset_factory(ShipmentContentsForm, extra=1)()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contents_formset = context['contents_formset']

        if contents_formset.is_valid():
            self.object = form.save()  # Сохраняем Shipment
            for content_form in contents_formset:
                if content_form.cleaned_data.get('product') and content_form.cleaned_data.get('quantity'):
                    ShipmentContents.objects.create(
                        shipment=self.object,
                        product=content_form.cleaned_data['product'],
                        quantity=content_form.cleaned_data['quantity']
                    )
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = "products/detail_shipment.html"
    context_object_name = "shipment"
    queryset = Shipment.objects.with_contents()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_form"] = ShipmentUpdateForm()
        return context

class ShipmentUpdateView(LoginRequiredMixin, BaseUpdateView):
    model = Shipment
    form_class = ShipmentUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "products:detail_shipment",
            kwargs={'pk': self.object.pk},
        )
