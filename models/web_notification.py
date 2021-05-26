from django.db import models
from django.utils.translation import gettext as _

from base.models.person import Person
from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes


class WebNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=NotificationTypes.WEB_TYPE.name)

    def create(self, person: Person, payload: str):
        """Create the Web Notification with the given person and payload.
        :param person: The Person object to send the notification to.
        :param payload: The payload of the notification.
        :return: The newly created WebNotification object.
        """

        return super().create(
            type=NotificationTypes.WEB_TYPE.name,
            person=person,
            payload=payload,
        )


class WebNotification(Notification):
    """Web notification base model."""

    objects = WebNotificationManager()

    class Meta:
        verbose_name = _("Web notification")
        proxy = True
