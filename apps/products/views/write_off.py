from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, DetailView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType

from ..models import WriteOff, ProductActivity, Storage
from ..forms import WriteOffForm, ProductActivityForm
from django.forms import formset_factory

class WriteOffListView(LoginRequiredMixin, ListView):
    """WriteOff list class-based view."""

    model = WriteOff
    template_name = "products/list_write_offs.html"
    context_object_name = "write_offs"
    paginate_by = 10


class WriteOffCreateView(LoginRequiredMixin, CreateView):
    model = WriteOff
    form_class = WriteOffForm
    template_name = 'products/create_write_off.html'
    success_url = reverse_lazy('products:list_write_offs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['contents_formset'] = formset_factory(ProductActivityForm, extra=1)(self.request.POST)
        else:
            context['contents_formset'] = formset_factory(ProductActivityForm, extra=1)()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contents_formset = context['contents_formset']

        if contents_formset.is_valid():
            self.object = form.save()

            writeoff_content_type = ContentType.objects.get_for_model(WriteOff)
            cleaned_models = []
            for content_form in contents_formset:
                cleaned_product = content_form.cleaned_data.get('product')
                cleaned_quantity = content_form.cleaned_data.get('quantity')
                if cleaned_product and cleaned_quantity:
                    if cleaned_product.in_storage_quantity < cleaned_quantity:
                        form.add_error(
                            field=None,
                            error=ValidationError(
                                _(
                                    (
                                        "Current in stock quantity of"
                                        " %(product)s is less than"
                                        " %(over_quantity)d that you want to"
                                        " write off, %(actual_quantity)d is"
                                        " actual of it."
                                    )
                                ),
                                params={
                                    "product": cleaned_product,
                                    "over_quantity": cleaned_quantity,
                                    "actual_quantity": (
                                        cleaned_product.in_storage_quantity
                                    ),
                                },
                                code="invalid",
                            ),
                        )
                    cleaned_models.append(
                        ProductActivity(
                            content_type=writeoff_content_type,
                            object_id=self.object.id,
                            product=cleaned_product,
                            quantity=cleaned_quantity,
                        ),
                    )
            if form.errors:
                self.object.delete()
                return super().form_invalid(form)
            ProductActivity.objects.bulk_create(cleaned_models)
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WriteOffDetailView(LoginRequiredMixin, DetailView):
    model = WriteOff
    template_name = "products/detail_write_off.html"
    context_object_name = "write_off"
    queryset = WriteOff.objects.with_contents()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_storage"] = Storage.objects.first()
        return context

class WriteOffDeleteView(LoginRequiredMixin, DeleteView):
    model = WriteOff
    success_url = reverse_lazy("products:list_write_offs")
