from django.utils.timezone import now

from osis_notification.models import WebNotification as WebNotificationModel
from osis_notification.models.enums import NotificationStates


class WebNotification:
    """Web notification class. Only handle the sending process, the build process has
    to be implemented by the children class."""

    def build(self, content):
        raise NotImplementedError(
            "Implement this method to build the notification content"
        )

    @staticmethod
    def mark_as_read(notification: WebNotificationModel):
        """Mark the notification's state as 'read' and save the reading's datetime."""

        notification.state = NotificationStates.READ_STATE.name
        notification.read_datetime = now()
        notification.save()

    @staticmethod
    def process(notification: WebNotificationModel):
        """Process the notification by sending the web notification."""

        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_datetime = now()
        notification.save()
