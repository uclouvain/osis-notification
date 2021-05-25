from django.db import models
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes


class WebNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.WEB_TYPE.name)


class WebNotification(Notification):
    """Web notification base model."""

    objects = WebNotificationManager()

    class Meta:
        verbose_name = _("Web notification")
        proxy = True

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
