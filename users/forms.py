from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, ConfirmationCode


class AuthForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": "Ваш аккаунт не активирован",
    }

    class Meta:
        model = User
        fields = ("email", "password")


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class ConfirmationCodeForm(forms.ModelForm):
    class Meta:
        model = ConfirmationCode
        fields = ("code",)

    def clean_code(self):
        code_queryset = (
            ConfirmationCode.objects
            .filter(code__exact=self.cleaned_data.get("code"))
        )

        if not code_queryset.exists():
            raise ValidationError("Вы ввели неправильный код")

        return self.cleaned_data["code"]
