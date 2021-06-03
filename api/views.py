from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from osis_notification.api.permissions import IsNotificationRecipient
from osis_notification.api.serializers import WebNotificationSerializer
from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates


class NotificationSetPagination(LimitOffsetPagination):
    default_limit = 15


class SentNotificationListView(generics.ListAPIView):
    """Return all sent notifications associated to a specific user."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsNotificationRecipient,)
    pagination_class = NotificationSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(person__uuid=self.kwargs["person_uuid"])


class MarkNotificationAsReadView(generics.UpdateAPIView):
    """Mark a single given notification as read if the notification is sent. If the
    notification is already mark as sent, it marks it as sent."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsNotificationRecipient,)

    def get_object(self):
        return get_object_or_404(
            self.queryset,
            person__uuid=self.kwargs["person_uuid"],
            uuid=self.kwargs["notification_uuid"],
        )

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.state == NotificationStates.READ_STATE.name:
            notification.state = NotificationStates.SENT_STATE.name
            notification.read_at = None
        else:
            notification.state = NotificationStates.READ_STATE.name
            notification.read_at = now()
        notification.save()
        return super().update(request, *args, **kwargs)
