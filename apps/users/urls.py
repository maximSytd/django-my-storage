from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import ProfileView, UserUpdateView

app_name = "users"

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "update-account/",
        UserUpdateView.as_view(),
        name="update_user",
    ),
]
