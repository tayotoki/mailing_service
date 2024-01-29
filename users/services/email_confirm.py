import random

from django.core.mail import send_mail

from mailing.urls import app_name
from ..models import User, ConfirmationCode


def generate_random_code():
    random.seed()
    return random.randint(1000, 9999)


def send_confirmation_email(code: int, user: User) -> None:
    send_mail(
        subject="Подтверждение почты",
        message=(
            f"Вы зарегистрировались на сервисе {' '.join(app_name.strip().title().split('_'))}. "
            f"Чтобы подтвердить свою почту, введите данный проверочный код:\n {code}"
        ),
        from_email="mail_service@localhost",
        recipient_list=[user.email],
        fail_silently=False,
    )


def bind_user_and_code(user: User, code: int) -> None:
    user.save()
    confirmation_instance = ConfirmationCode(user=user, code=code)
    confirmation_instance.save()
