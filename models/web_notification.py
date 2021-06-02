from django.db import models
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationStates, NotificationTypes


class WebNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.WEB_TYPE.name)

    def pending(self):
        """Returns all the pending web notifications."""

        return (
            self.get_queryset()
            .filter(state=NotificationStates.PENDING_STATE.name)
            .order_by("created_at")
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
