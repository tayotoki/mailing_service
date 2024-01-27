from datetime import timedelta

from django.db import models

from ckeditor.fields import RichTextField
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime

from common.models import NULLABLE
from users.models import User

from .constants import MailingStatus, MailingPeriodicity
from .querysets import mailings, clients
from common.utils import datetime_format


class ModelWithOwner(models.Model):
    owner = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        null=True,
        editable=False
    )

    class Meta:
        abstract = True


class Client(models.Model):
    """Клиент"""

    email = models.EmailField(unique=True, verbose_name='почта')
    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        null=True,
        editable=False
    )

    objects = clients.ClientQuerySet().as_manager()

    def __str__(self):
        return f'{self.fullname} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_absolute_url(self):
        return reverse_lazy('mailing:client-detail', kwargs={'pk': self.pk})


class MailMessage(models.Model):
    """Наполнение рассылки"""

    title = models.CharField(max_length=150, verbose_name='тема письма')
    body = RichTextField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения рассылок'

    def get_absolute_url(self):
        return reverse_lazy('mailing:message-detail', kwargs={'pk': self.pk})


class MailLogger(models.Model):
    """Логгер сообщения"""

    time = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.CharField(max_length=150, verbose_name='статус попытки')
    mail_backend_response = models.CharField(max_length=150, verbose_name='ответ почтового сервера')

    message = models.ForeignKey(
        MailMessage,
        on_delete=models.SET_NULL,
        verbose_name='сообщение',
        related_name='mail_loggers',
        **NULLABLE,
    )

    def __str__(self):
        return f'[{self.time}]'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'


class MailingSettings(models.Model):
    """Настройка рассылки"""

    time = models.DateTimeField(verbose_name='время рассылки', default=timezone.now)
    periodicity = models.PositiveSmallIntegerField(
        verbose_name='периодичность рассылки',
        choices=MailingPeriodicity.choices,
        default=MailingPeriodicity.MONTH,
    )
    status = models.CharField(
        max_length=150,
        verbose_name='статус',
        choices=MailingStatus.choices,
        default=MailingStatus.CREATED,
    )

    clients = models.ManyToManyField(
        Client, verbose_name='клиенты', related_name='mailings', related_query_name='mailing'
    )

    messages = models.ManyToManyField(
        MailMessage, verbose_name='сообщения', related_name='mailings', related_query_name='mailing'
    )

    objects = mailings.MailingQuerySet.as_manager()

    @property
    # @datetime_format(fail_silently=True)
    def next_time(self) -> datetime:
        "Следующее дата/время рассылки"

        return self.time + timedelta(days=self.periodicity)

    def __str__(self):
        return f'Рассылка на {self.time.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'

    def get_absolute_url(self):
        return reverse_lazy('mailing:mailing-detail', kwargs={'pk': self.pk})
