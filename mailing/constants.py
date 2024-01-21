from django.db.models import TextChoices, IntegerChoices


class MailingStatus(TextChoices):
    COMPLETED = "completed", "завершена"
    CREATED = "created", "создана"
    LAUNCHED = "launched", "запущена"


class MailingPeriodicity(IntegerChoices):
    DAY = 1, 'раз в день'
    WEEK = 7, 'раз в неделю'
    MONTH = 30, 'раз в месяц'
