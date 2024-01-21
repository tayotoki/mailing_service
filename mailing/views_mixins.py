from .forms.mailing import MailingSettingsForm
from .models import MailingSettings
from .services import mailing_run_service


class MailingCreateUpdateMixin:
    model = MailingSettings
    form_class = MailingSettingsForm
    queryset = MailingSettings.objects.prefetch_related("messages", "clients")

    def get_success_url(self):
        mailing_run_service.start_single_mailing(mailing=self.object)
        return super().get_success_url()
