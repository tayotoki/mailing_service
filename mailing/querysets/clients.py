from django.db.models import QuerySet


class ClientQuerySet(QuerySet):
    def unique_clients(self):
        return self.all().distinct()
