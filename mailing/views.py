from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from blog.models import Post
from .forms.mailing import ClientForm, MessageForm, MailingBlockForm
from .models import MailingSettings, Client, MailMessage
from .views_mixins import (
    MailingCreateUpdateMixin,
    ForOwnerOrStufOnlyMixin,
    BindOwnerMixin,
    LimitedFormMixin,
    RelatedQuerySetMixin,
)


class MailingListView(generic.ListView):
    template_name = 'mailing/index.html'
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        cache_key = "extra_context"
        extra_context = cache.get(cache_key)

        if not extra_context:
            extra_context = {
                "mailings_count": self.model.objects.mailings_count(),
                "active_mailings_count": self.model.objects.active_mailings_count(),
                "unique_clients_count": Client.objects.unique_clients().count(),
                "random_blog_posts": Post.posts.random_blog_posts(count=3),
            }
            cache.set(cache_key, extra_context, 60 * 10)

        context.update(extra_context)

        return context


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_detail.html'
    form_class = MailingBlockForm

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            mailing = self.get_object()
            mailing.is_active = not mailing.is_active
            mailing.save()
            return redirect(reverse_lazy("mailing:mailing-list"))


class MailingUserListView(ForOwnerOrStufOnlyMixin, LoginRequiredMixin, generic.ListView):
    model = MailingSettings
    template_name = "mailing/mailings_list.html"
    paginate_by = 10


class MailingCreateView(
    LoginRequiredMixin,
    BindOwnerMixin,
    RelatedQuerySetMixin,
    LimitedFormMixin,
    MailingCreateUpdateMixin,
    generic.CreateView,
):
    template_name = 'mailing/mailing_create.html'


class MailingUpdateView(
    LoginRequiredMixin,
    RelatedQuerySetMixin,
    LimitedFormMixin,
    MailingCreateUpdateMixin,
    generic.UpdateView,
):
    template_name = "mailing/mailing_update.html"


class ClientCreateView(LoginRequiredMixin, BindOwnerMixin, generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_create.html"


class ClientListView(ForOwnerOrStufOnlyMixin, LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = "mailing/clients_list.html"
    paginate_by = 10


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_update.html"


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class MessageCreateView(LoginRequiredMixin, BindOwnerMixin, generic.CreateView):
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


class MessageListView(ForOwnerOrStufOnlyMixin, LoginRequiredMixin, generic.ListView):
    model = MailMessage
    template_name = "mailing/messages_list.html"
    paginate_by = 10


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MailingSettings
    success_url = reverse_lazy("mailing:mailing-list")


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MailMessage
    success_url = reverse_lazy("mailing:message-list")


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client-list")
