from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User
from .forms import UserUpdateForm
from apps.products.models import Storage


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "users/profile.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_update_form"] = UserUpdateForm()
        context["has_storage"] = Storage.objects.first()
        return context

    def get_object(self, queryset = None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/update_user.html"
    model = User
    context_object_name = "user"
    form_class = UserUpdateForm

    def get_object(self, queryset = None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")
