# Generated by Django 4.1 on 2024-02-11 16:22

from django.db import migrations, models
import django.db.models.manager
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid_field",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Заголовок")),
                ("slug", models.CharField(max_length=100)),
                ("content", models.TextField(verbose_name="Содержимое")),
                (
                    "preview",
                    models.ImageField(upload_to="previews", verbose_name="Превью"),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликовано"),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(default=0, verbose_name="Количество просмотров"),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
            },
            managers=[
                ("posts", django.db.models.manager.Manager()),
            ],
        ),
    ]
