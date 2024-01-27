from django.db.models import QuerySet, Q
from django.utils import timezone

from ..constants import MailingStatus


class MailingQuerySet(QuerySet):
    def ready_for_sending(self):
        """Возвращает кверисет запущенных рассылок,
        которые готовы к отправке"""

        return self.filter(Q(time__lte=timezone.now()) & Q(status=MailingStatus.LAUNCHED))

    def mailings_count(self) -> int:
        return self.all().count()

    def active_mailings_count(self) -> int:
        return self.filter(status=MailingStatus.LAUNCHED).count()
