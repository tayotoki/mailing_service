from django.db import models

from ckeditor.fields import RichTextField

from common.models import NULLABLE

from .constants import MailingStatus, MailingPeriodicity


class Client(models.Model):
    """Клиент"""
    email = models.EmailField(unique=True, verbose_name='почта')
    fullname = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.fullname} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailMessage(models.Model):
    """Наполнение рассылки"""
    title = models.CharField(max_length=150, verbose_name='тема письма')
    body = RichTextField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения рассылок'


class MailLogger(models.Model):
    """Логгер сообщения"""
    time = models.DateTimeField(verbose_name='дата и время последней попытки', **NULLABLE)
    status = models.CharField(max_length=150, verbose_name='статус попытки')
    mail_backend_response = models.CharField(max_length=150, verbose_name='ответ почтового сервера')

    message = models.OneToOneField(
        MailMessage,
        on_delete=models.CASCADE,
        verbose_name='сообщение',
        primary_key=True,
        related_name='mail_logger'
    )

    def __str__(self):
        return f'[{self.time}] {self.status} {self.mail_backend_response}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'


class MailingSettings(models.Model):
    """Настройка рассылки"""
    time = models.DateTimeField(verbose_name='время рассылки', **NULLABLE)
    periodicity = models.PositiveSmallIntegerField(
        verbose_name='периодичность рассылки',
        choices=MailingPeriodicity.choices,
        default=MailingPeriodicity.MONTH
    )
    status = models.CharField(
        verbose_name='статус',
        choices=MailingStatus.choices,
        default=MailingStatus.CREATED,
        editable=False
    )

    clients = models.ManyToManyField(
        Client,
        verbose_name='клиенты',
        related_name='mailings',
        related_query_name='mailing'
    )

    messages = models.ManyToManyField(
        MailMessage,
        verbose_name='сообщения',
        related_name='mailings',
        related_query_name='mailing'
    )

    def __str__(self):
        return f'Периодичность: {self.periodicity}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
