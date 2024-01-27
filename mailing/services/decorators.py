from collections.abc import Callable

from django.core import mail


def keep_mail_backend_connection(func: Callable):
    def wrapper(*args, **kwargs):
        with mail.get_connection() as connection:
            return func(*args, connection=connection, **kwargs)

    return wrapper
