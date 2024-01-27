from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View

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


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, MailingCreateUpdateMixin, generic.CreateView):
    template_name = 'mailing/mailing_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, MailingCreateUpdateMixin, generic.UpdateView):
    template_name = "mailing/mailing_update.html"


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_create.html"


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_update.html"


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = MailMessage
    form_class = MessageForm
    template_name = "mailing/message_create.html"


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = MailMessage
    template_name = "mailing/message_detail.html"


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MailMessage
    form_class = MessageForm
    template_name = "mailing/message_update.html"
