from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import ShipmentContents
from ..forms import (

    ShipmentUpdateForm,
)
from ..forms import ShipmentContentsForm


class ShipmentContentsUpdateView(LoginRequiredMixin, UpdateView):
    model = ShipmentContents
    form_class = ShipmentContentsForm
    template_name = "products/detail_shipment_contents.html"
    context_object_name = "shipment_content"

    def get_success_url(self):
        return reverse_lazy(
            "products:detail_shipment",
            kwargs={'pk': self.object.pk},
        )
