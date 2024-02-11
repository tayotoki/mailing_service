import uuid

from django.db import models

from .managers import PostsManager


class Post(models.Model):
    # Fields.
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.CharField(max_length=100, null=False)
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to="previews", verbose_name="Превью")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)
    views_count = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    # Managers.
    posts = PostsManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title
