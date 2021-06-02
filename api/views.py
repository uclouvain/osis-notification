from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from osis_notification.api.permissions import IsNotificationRecipient
from osis_notification.api.serializers import WebNotificationSerializer
from osis_notification.models import WebNotification


class NotificationSetPagination(LimitOffsetPagination):
    default_limit = 15


class SentNotificationListView(generics.ListAPIView):
    """Return all sent notifications associated to a specific user."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsNotificationRecipient,)
    pagination_class = NotificationSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(person__uuid=self.kwargs["uuid"])
