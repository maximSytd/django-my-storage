from django.views.generic import CreateView, UpdateView, ListView
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Shipment, ShipmentContents
from ..forms import ShipmentForm, ShipmentContentsForm

class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'products/create_shipment.html'
    success_url = reverse_lazy('index')

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

# Создаем formset_factory для ShipmentContentsForm


# class ShipmentCreateView(LoginRequiredMixin, CreateView):
#     """Shipment create class-based view."""

#     model = Shipment
#     template_name = "products/create_shipment.html"
#     success_url = reverse_lazy("products:list_suppliers")


class ShipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Shipment
    template_name = "products/update_shipment.html"
    success_url = reverse_lazy("products:list_suppliers")



class ShipmentListView(LoginRequiredMixin, ListView):
    """Shipment list class-based view."""

    model = Shipment
    template_name = "products/list_shipments.html"
    context_object_name = "shipments"