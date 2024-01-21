import threading
from typing import Optional

from django.core.mail import send_mail
from django.db.models import F, QuerySet
from django.utils import timezone

from mailing.models import MailingSettings, MailLogger


def send_email(clients, message, loggers) -> None:
    """Отправка конкретного сообщения клиентам.
    Создаются объекты-логгеры для каждого сообщения (без сохранения в БД)"""
    logger = MailLogger(time=timezone.now(), message=message, status="", mail_backend_response="")

    try:
        send_mail(
            subject=message.title,
            message=message.body,
            from_email="mail_service@localhost",
            recipient_list=[client["email"] for client in clients],
        )

    except Exception as e:
        logger.mail_backend_response = f"{e}"
        logger.status = "неудачная отправка"

    else:
        logger.status = "удачная отправка"

    finally:
        loggers.append(logger)


def start_mailing(ready_mailings: Optional[QuerySet] = None) -> None:
    """Запуск переданных рассылок.
    Создаются записи базе данных для всех логгеров сообщений"""
    if ready_mailings is None:
        ready_mailings = MailingSettings.objects.ready_for_sending().prefetch_related(
            "clients", "messages"
        )

    loggers = []

    for mailing in ready_mailings:
        clients = mailing.clients.values("email", "fullname")

        for message in mailing.messages.all():
            # Отправка сообщений будет происходить в отдельных потоках,
            # чтобы не блокировать повышенным таймаутом основной поток.
            thread = threading.Thread(target=send_email, args=(clients, message, loggers))
            thread.start()
            thread.join()

    ready_mailings.update(time=timezone.now() + timezone.timedelta(days=1) * F("periodicity"))
    MailLogger.objects.bulk_create(loggers)


def start_single_mailing(mailing: MailingSettings) -> None:
    """Запуск одной рассылки"""
    mailing: QuerySet = MailingSettings.objects.filter(pk=mailing.id).prefetch_related(
        "clients", "messages"
    )

    mailing_instance: MailingSettings = mailing.get()

    if mailing_instance.time <= timezone.now() < mailing_instance.next_time:
        start_mailing(ready_mailings=mailing)
