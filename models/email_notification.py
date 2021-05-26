from django.db import models
from django.utils.translation import gettext as _

from base.models.person import Person
from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes


class EmailNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.EMAIL_TYPE.name)

    def create(self, person: Person, payload: str):
        """Create the Email Notification with the given person and payload.
        :param person: The Person object to send the notification to.
        :param payload: The payload of the notification.
        :return: The newly created EmailNotification object.
        """

        return super().create(
            type=NotificationTypes.EMAIL_TYPE.name,
            person=person,
            payload=payload,
        )


class EmailNotification(Notification):
    """Email notification model."""

    objects = EmailNotificationManager()

    class Meta:
        verbose_name = _("Email notification")
        proxy = True
