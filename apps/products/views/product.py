from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from ..models import Product, Category, Shipment, ShipmentContents
from ..filters import ProductFilter
from ..forms import CategoryForm, ProductForm

class ProductListView(LoginRequiredMixin, FilterView):
    model = Product
    template_name = "products/list_products.html"
    filterset_class = ProductFilter
    context_object_name = "products"
    queryset = Product.objects.with_quantity()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_form"] = CategoryForm()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "products/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:list_products")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "products/update_product.html"
    form_class = ProductForm
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category_form"] = CategoryForm()
        return context

    def get_success_url(self):
        return reverse_lazy(
            "products:detail_product",
            kwargs={
                "pk": self.object.pk,
            },
        )


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/detail_product.html"
    context_object_name = "product"
    queryset = Product.objects.with_quantity()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category_form"] = CategoryForm()
        context["shipments"] = Shipment.objects.prefetch_related(
            "ordered_by",
        ).filter(
            shipment_contents__in=ShipmentContents.objects.filter(
                product=self.object,
            ),
        ).distinct()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
