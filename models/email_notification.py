from django.db import models
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationStates, NotificationTypes


class EmailNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.EMAIL_TYPE.name)

    def pending(self):
        """Returns all the pending email notifications."""

        return self.get_queryset().filter(
            state=NotificationStates.PENDING_STATE.name
        )

    def create(self, **kwargs):
        """Create the Email Notification with the given person and payload.

        :param kwargs: See below ;
            person (Person): The Person object to send the notification to.
            payload (str): The payload of the notification.

        :return: The newly created EmailNotification object.
        """

        return super().create(
            type=NotificationTypes.EMAIL_TYPE.name,
            person=kwargs.get("person"),
            payload=kwargs.get("payload"),
        )


class EmailNotification(Notification):
    """Email notification model."""

    objects = EmailNotificationManager()

    class Meta:
        verbose_name = _("Email notification")
        proxy = True
