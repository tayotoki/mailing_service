from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView

from .forms import UserRegistrationForm, ConfirmationCodeForm
from .models import User
from .views_mixins import ConfirmationCodeMixin, SuccessConfirmationMixin


class RegisterView(ConfirmationCodeMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/user_registration.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("mailing:index"))
        return super().get(request, *args, **kwargs)


class ConfirmationCodeView(SuccessConfirmationMixin, FormView):
    form_class = ConfirmationCodeForm
    success_url = reverse_lazy("mailing:index")
    template_name = "users/confirmation_code_form.html"


class UserProfileView(DetailView):
    model = User
    template_name = "users/user_profile.html"
