from django.views import generic

from .forms.mailing import ClientForm, MessageForm
from .models import MailingSettings, Client, MailMessage
from .views_mixins import MailingCreateUpdateMixin


class MailingListView(generic.ListView):
    template_name = 'mailing/index.html'
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["mailings_count"] = self.model.objects.mailings_count()
        context["active_mailings_count"] = self.model.objects.active_mailings_count()
        context["unique_clients_count"] = Client.objects.unique_clients().count()
        return context


class MailingDetailView(generic.DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'


class MailingCreateView(MailingCreateUpdateMixin, generic.CreateView):
    template_name = 'mailing/mailing_create.html'


class MailingUpdateView(MailingCreateUpdateMixin, generic.UpdateView):
    template_name = "mailing/mailing_update.html"


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_create.html"


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_update.html"


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class MessageCreateView(generic.CreateView):
    model = MailMessage
    form_class = MessageForm
    template_name = "mailing/message_create.html"


class MessageDetailView(generic.DetailView):
    model = MailMessage
    template_name = "mailing/message_detail.html"


class MessageUpdateView(generic.UpdateView):
    model = MailMessage
    form_class = MessageForm
    template_name = "mailing/message_update.html"
