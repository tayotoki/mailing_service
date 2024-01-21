from django.urls import path

from .views import (
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    ClientCreateView,
    ClientDetailView,
    ClientUpdateView, MessageCreateView, MessageDetailView, MessageUpdateView,
)
from .apps import MailingConfig

app_name = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing-update'),
    path('client/create', ClientCreateView.as_view(), name='client-create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('messages/create', MessageCreateView.as_view(), name='message-create'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]