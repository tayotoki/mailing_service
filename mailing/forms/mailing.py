from ckeditor import widgets
from django import forms
from django.forms import SplitDateTimeWidget, SplitDateTimeField, SelectMultiple
from django.utils import timezone

from ..models import Client, MailMessage, MailingSettings


class MessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = "__all__"
        widgets = {"body": widgets.CKEditorWidget()}


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MailingSettingsForm(forms.ModelForm):
    time = SplitDateTimeField(
        widget=SplitDateTimeWidget(
            date_format='%d.%m.%Y',
            time_format="%H:%M",
            date_attrs={"type": "date", "value": timezone.localdate()},
            time_attrs={"type": "time", "value": timezone.localtime().strftime("%H:%M")},
        ),
        label="Время рассылки",
    )

    class Meta:
        model = MailingSettings
        exclude = ("is_active",)

        widgets = {
            "messages": SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": "4",
                    "multiple aria-label": "Выбрать сообщения",
                }
            ),
            "clients": SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": "4",
                    "multiple aria-label": "Выбрать клиентов",
                }
            ),
        }


class MailingBlockForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ("is_active",)
