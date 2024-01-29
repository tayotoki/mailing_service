from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import RegisterView, UserProfileView, ConfirmationCodeView, UserListView
from .apps import UsersConfig
from .forms import AuthForm

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListView.as_view(), name="users-list"),
    path("register/", RegisterView.as_view(), name="users-register"),
    path(
        "login/", LoginView.as_view(
            template_name="users/user_login.html",
            authentication_form=AuthForm,
            redirect_authenticated_user=True,
            next_page="/"
        ), name="users-login"
    ),
    path("logout/", LogoutView.as_view(next_page="/"), name="users-logout"),
    path("profile/<int:pk>", UserProfileView.as_view(), name="users-profile"),
    path("confirm-<uuid:uuid>/", ConfirmationCodeView.as_view(), name="users-confirm"),
]
