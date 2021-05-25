from django.db import models
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes


class EmailNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.EMAIL_TYPE.name)


class EmailNotification(Notification):
    """Email notification model."""

    objects = EmailNotificationManager()

    class Meta:
        verbose_name = _("Email notification")
        proxy = True

    @classmethod
    def create(cls, person, content):
        """Create the Email Notification with the given person and content.
        :param person: The Person object to send the notification to.
        :param content: The content of the notification.
        :return: The newly created EmailNotification object.
        """

        return cls(
            person=person,
            notification_type=NotificationTypes.EMAIL_TYPE.name,
            payload=content,
        )
