from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User
from .forms import UserInitialsUpdateForm


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "users/profile.html"
    model = User
    context_object_name = "user"

    def get_object(self, queryset = None):
        return self.request.user


class UserInitialsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/update_user.html"
    model = User
    context_object_name = "user"
    form_class = UserInitialsUpdateForm

    def get_object(self, queryset = None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy("users:profile")
    

class UserAvatarUpdateView(LoginRequiredMixin, UpdateView):
    fields = ("avatar",)
    model = User

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")