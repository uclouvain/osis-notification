from django.db import models
from django.utils.translation import gettext_lazy as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationStates, NotificationTypes


class WebNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.WEB_TYPE.name)

    def order_by_sent_first(self):
        """Notifications with SENT_STATE will come first"""
        return self.get_queryset().order_by("-state", "created_at")

    def pending(self):
        """Returns all the pending web notifications."""
        return (
            self.get_queryset()
            .filter(state=NotificationStates.PENDING_STATE.name)
            .order_by("created_at")
        )

    def sent(self):
        """Return all the sent notifications, including all the read notifications."""
        return self.order_by_sent_first().filter(
            state__in=[
                NotificationStates.SENT_STATE.name,
                NotificationStates.READ_STATE.name,
            ],
        )

    def create(self, **kwargs):
        """Create the Web Notification with the given person and payload.

        :param kwargs: See below ;
            person (Person): The Person object to send the notification to.
            payload (str): The payload of the notification.

        :return: The newly created WebNotification object.
        """

        return super().create(
            type=NotificationTypes.WEB_TYPE.name,
            person=kwargs.get("person"),
            payload=kwargs.get("payload"),
        )


class WebNotification(Notification):
    """Web notification base model."""

    objects = WebNotificationManager()

    class Meta:
        verbose_name = _("Web notification")
        proxy = True
