from django.db import models
from django.utils.translation import gettext as _

from base.models.person import Person
from osis_notification.models.enums import (
    NotificationStates,
    NotificationTypes,
)


class Notification(models.Model):
    """Base class for a notification"""

    type = models.CharField(
        _("Type"),
        choices=NotificationTypes.choices(),
        max_length=25,
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="+")
    payload = models.TextField(_("Payload"))
    state = models.CharField(
        _("State"),
        choices=NotificationStates.choices(),
        default=NotificationStates.PENDING_STATE.name,
        max_length=25,
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    sent_at = models.DateTimeField(verbose_name=_("Sent at"), editable=False, null=True)
    read_at = models.DateTimeField(verbose_name=_("Read at"), editable=False, null=True)

    class Meta:
        ordering = ["-created_at"]
