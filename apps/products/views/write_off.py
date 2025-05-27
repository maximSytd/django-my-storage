from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType

from ..models import WriteOff, ProductActivity
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

            for content_form in contents_formset:
                if content_form.cleaned_data.get('product') and content_form.cleaned_data.get('quantity'):
                    ProductActivity.objects.create(
                        content_type=writeoff_content_type,
                        object_id=self.object.id,
                        product=content_form.cleaned_data['product'],
                        quantity=content_form.cleaned_data['quantity']
                    )
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WriteOffDetailView(LoginRequiredMixin, DetailView):
    model = WriteOff
    template_name = "products/detail_write_off.html"
    context_object_name = "write_off"
    queryset = WriteOff.objects.with_contents()

class WriteOffDeleteView(LoginRequiredMixin, DeleteView):
    model = WriteOff
    success_url = reverse_lazy("products:list_write_offs")
