import uuid

from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse

from .models import User, ConfirmationCode
from .services.email_confirm import generate_random_code, send_confirmation_email, bind_user_and_code


class SuccessConfirmationMixin:
    def form_valid(self, form):
        code = form.cleaned_data.get("code")
        user = User.objects.filter(confirmation_code__code=code).select_related("confirmation_code").first()
        user.is_active = True
        user.confirmation_code.delete()
        user.save()
        login(self.request, user)

        return super().form_valid(form)


class ConfirmationCodeMixin:
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        confirmation_code = generate_random_code()
        send_confirmation_email(code=confirmation_code, user=user)
        bind_user_and_code(user=user, code=confirmation_code)

        return redirect(reverse("users:users-confirm", kwargs={"uuid": uuid.uuid4()}))  # unique link
