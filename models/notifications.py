from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _

from base.models.person import Person

# Notification's types
EMAIL_TYPE = "email"
WEB_TYPE = "web"

# Notification's states
PENDING_STATE = "pending"
SENT_STATE = "sent"
READ_STATE = "read"


class Notification(models.Model):
    """Base class for a notification"""

    TYPE_CHOICES = (
        (EMAIL_TYPE, _("Email notification")),
        (WEB_TYPE, _("Web notification")),
    )
    STATE_CHOICES = (
        (PENDING_STATE, _("Pending")),
        (SENT_STATE, _("Sent")),
        (READ_STATE, _("Read")),
    )

    notification_type = models.CharField(_("Type"), choices=TYPE_CHOICES, max_length=10)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='+')
    payload = models.TextField(_("Payload"))
    state = models.CharField(
        _("State"), choices=STATE_CHOICES, default=PENDING_STATE, max_length=10
    )

    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    sent_datetime = models.DateTimeField(
        verbose_name=_("Sent at"), editable=False, null=True
    )
    read_datetime = models.DateTimeField(
        verbose_name=_("Read at"), editable=False, null=True
    )

    class Meta:
        ordering = ["-created"]

    def mark_as_read(self):
        """Mark the notification's state as 'read' and save the reading's datetime."""

        self.state = READ_STATE
        self.read_datetime = now()
        self.save()

    def process(self):
        raise NotImplementedError("Implement this method to process the notification")


class WebNotification(Notification):
    """Web notification model. Only handle the sending process, the build process has
    to be implemented by the children class."""

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
            notification_type=WEB_TYPE,
            person=person,
            payload=content,
        )

    def process(self):
        """Process the notification by sending the web notification."""

        self.state = SENT_STATE
        self.save()
