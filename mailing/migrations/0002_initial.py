# Generated by Django 4.1 on 2024-02-11 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("mailing", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="mailmessage",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="maillogger",
            name="message",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mail_loggers",
                to="mailing.mailmessage",
                verbose_name="сообщение",
            ),
        ),
        migrations.AddField(
            model_name="mailingsettings",
            name="clients",
            field=models.ManyToManyField(
                related_name="mailings",
                related_query_name="mailing",
                to="mailing.client",
                verbose_name="клиенты",
            ),
        ),
        migrations.AddField(
            model_name="mailingsettings",
            name="messages",
            field=models.ManyToManyField(
                related_name="mailings",
                related_query_name="mailing",
                to="mailing.mailmessage",
                verbose_name="сообщения",
            ),
        ),
        migrations.AddField(
            model_name="mailingsettings",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
    ]
