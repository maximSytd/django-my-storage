from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from ..models import Category
from ..forms import CategoryForm

class BaseCategoryView(LoginRequiredMixin):
    success_url = reverse_lazy("products:list_products")


class CategoryListView(BaseCategoryView, FilterView):
    model = Category


class CategoryCreateView(BaseCategoryView, CreateView):
    model = Category
    form_class = CategoryForm


class CategoryUpdateView(BaseCategoryView, UpdateView):
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(BaseCategoryView, DeleteView):
    model = Category
