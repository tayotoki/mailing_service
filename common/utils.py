from collections.abc import Callable
from time import strptime
from typing import Optional
from datetime import datetime


def get_filename(filename, request):
    return filename.upper()


def datetime_format(format: str = "%d.%m.%Y %H:%M", fail_silently: bool = False):  # noqa
    def decorator(func: Callable):
        def wrapper(self):
            time = func(self)

            if isinstance(time, datetime):
                time = time.strftime(format)
            if not fail_silently:
                raise TypeError(f"{time.__class__} not supported class, use datetime.datetime")

            return time

        return wrapper
    return decorator
