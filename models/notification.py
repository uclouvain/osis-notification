from django.db import models
from django.utils.translation import gettext as _

from base.models.person import Person
from osis_notification.models.enums import (
    NotificationStates,
    NotificationTypes,
)


class Notification(models.Model):
    """Base class for a notification"""

    notification_type = models.CharField(
        _("Type"),
        choices=NotificationTypes.choices(),
        max_length=10,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='+')
    payload = models.TextField(_("Payload"))
    state = models.CharField(
        _("State"),
        choices=NotificationStates.choices(),
        default=NotificationStates.PENDING_STATE.name,
        max_length=10,
    )

    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    sent_datetime = models.DateTimeField(
        verbose_name=_("Sent at"),
        editable=False,
        null=True,
    )
    read_datetime = models.DateTimeField(
        verbose_name=_("Read at"),
        editable=False,
        null=True,
    )

    class Meta:
        ordering = ["-created"]
