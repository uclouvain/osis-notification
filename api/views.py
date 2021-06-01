from rest_framework import generics

from osis_notification.api.permissions import IsNotificationRecipient
from osis_notification.api.serializers import WebNotificationSerializer
from osis_notification.models import WebNotification


class SentNotificationListView(generics.ListAPIView):
    """Return all sent notifications associated to a specific user."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsNotificationRecipient,)

    def get_queryset(self):
        return super().get_queryset().filter(person__uuid=self.kwargs["uuid"])
