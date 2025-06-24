from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from ..models import Storage
from ..forms import StorageForm

class AdminAccessMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StorageCreateView(LoginRequiredMixin, CreateView):
    """DeparturePoint create class-based view."""

    model = Storage
    template_name = "products/create_storage.html"
    form_class = StorageForm
    success_url = reverse_lazy("users:profile")


class StorageUpdateView(LoginRequiredMixin, UpdateView):
    model = Storage
    template_name = "products/update_storage.html"
    form_class = StorageForm
    context_object_name = "storage"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset = ...):
        return Storage.objects.first()
