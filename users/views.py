from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import UserRegistrationForm, ConfirmationCodeForm
from .models import User, UserProfile
from .views_mixins import ConfirmationCodeMixin, SuccessConfirmationMixin, StaffRequiredMixin


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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "users/user_profile.html"

    # TODO: пересмотреть шаблоны, убрать переопределение методов (костыль).

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        staff = False
        other_user = False

        if all(
            (
                self.request.user.is_staff,
                self.request.user != self.get_object().user,
                not self.get_object().user.is_staff,
            )
        ):
            staff = True
        elif self.request.user != self.get_object().user:
            other_user = True

        context["staff"] = staff
        context["other_user"] = other_user

        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.object = self.get_object()
            self.object.user.is_active = False
            self.object.user.save()
            return redirect(reverse("users:users-list"))
        return HttpResponse(status=403)


class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
