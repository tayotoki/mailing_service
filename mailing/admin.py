from django.contrib import admin

from .models import MailingSettings, MailMessage, MailLogger, Client


admin.site.register(MailMessage)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ("next_time",)
    list_display = ("time", "periodicity", "next_time", "status", "owner", "is_active")

    def next_time(self, obj):
        return obj.next_time

    next_time.short_description = "Следующая дата/время рассылки"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "owner")


@admin.register(MailLogger)
class MailLoggerAdmin(admin.ModelAdmin):
    list_display = ("time", "status", "mail_backend_response", "message")
