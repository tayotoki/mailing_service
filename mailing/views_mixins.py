from django.db.models import Prefetch, Q

from .forms.mailing import MailingSettingsForm
from .models import MailingSettings, Client, MailMessage
from .services import mailing_run_service


class MailingCreateUpdateMixin:
    model = MailingSettings
    form_class = MailingSettingsForm

    def get_success_url(self):
        mailing_run_service.start_single_mailing(mailing=self.object)
        return super().get_success_url()


class ForOwnerOrStufOnlyMixin:
    def get_queryset(self):
        user_filter = self.request.GET.get('user')

        default_filter = Q(owner__pk=self.request.user.pk)

        if user_filter:
            default_filter = Q(owner__pk=user_filter)

        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.request.user.is_staff:
            return self.model.objects.filter(default_filter).select_related("owner")

        return self.model.objects.filter(owner__is_staff=False).select_related("owner")


class BindOwnerMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LimitedFormMixin:
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
            my_form_class = form_class(**self.get_form_kwargs())
            # TODO: оптимизировать 2 запроса к БД.
            my_form_class["clients"].field.queryset = Client.objects.filter(
                owner=self.request.user
            ).prefetch_related("mailings")
            my_form_class["messages"].field.queryset = MailMessage.objects.filter(
                owner=self.request.user
            ).prefetch_related("mailings")
            return my_form_class


class RelatedQuerySetMixin:
    def get_queryset(self):
        q = Q(owner=self.request.user)

        queryset = MailingSettings.objects.filter(q, pk=self.kwargs.get("pk")).prefetch_related(
            Prefetch("clients", queryset=Client.objects.filter(q)),
            Prefetch("messages", queryset=MailMessage.objects.filter(q)),
        )

        return queryset
