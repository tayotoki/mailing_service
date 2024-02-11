from collections.abc import Sequence

from django.db import models
from django.db.models import F, Q


class PostsManager(models.Manager):
    def published(self):
        """Return queryset with only published posts"""
        return self.get_queryset().filter(is_published=True)

    def not_published(self):
        return self.get_queryset().filter(is_published=False)

    def best_five_posts(self):
        """Return queryset with 5 posts with the highest views"""
        return self.published().order_by("-views_count")[:5]

    def get_search_results(self, search_term):
        return self.published().filter(
            Q(title__iregex=search_term) |
            Q(content__icontains=search_term)
        ).order_by("-created_at")

    def update_views(self, pk: int | Sequence[int]):
        """Increase post | posts views_count field by 1"""
        if isinstance(pk, (str, bytes)):
            return

        if isinstance(pk, int):
            queryset = self.published().filter(pk=pk)
            if queryset:
                queryset.update(views_count=F("views_count") + 1)
                post = queryset.get()
                post.save()  # Trigger post_save signal in email_service.

        elif isinstance(pk, Sequence):
            self.published().filter(pk__in=pk).update(views_count=F("views_count") + 1)