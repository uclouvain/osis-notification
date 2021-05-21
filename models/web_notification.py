from django.db import models
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import (
    NotificationStates,
    NotificationTypes,
)


class WebNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.WEB_TYPE.name)


class WebNotification(Notification):
    """Web notification model. Only handle the sending process, the build process has
    to be implemented by the children class."""

    objects = WebNotificationManager()

    class Meta:
        verbose_name = _("Web notification")
        proxy = True

    def build(self, content):
        raise NotImplementedError(
            "Implement this method to build the notification content"
        )

    @classmethod
    def create(cls, person, content):
        """Create the Web Notification with the given person and content.
        :param person: The Person object to send the notification to.
        :param content: The content of the notification.
        :return: The newly created WebNotification object.
        """

        return cls(
            notification_type=NotificationTypes.WEB_TYPE.name,
            person=person,
            payload=content,
        )

    def process(self):
        """Process the notification by sending the web notification."""

        self.state = NotificationStates.SENT_STATE.name
        self.save()
