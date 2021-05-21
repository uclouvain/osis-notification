import email
from html import unescape

from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.timezone import now
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

    def mark_as_read(self):
        """Mark the notification's state as 'read' and save the reading's datetime."""

        self.state = NotificationStates.READ_STATE.name
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
            notification_type=NotificationTypes.WEB_TYPE.name,
            person=person,
            payload=content,
        )

    def process(self):
        """Process the notification by sending the web notification."""

        self.state = NotificationStates.SENT_STATE.name
        self.save()


class EmailNotification(Notification):
    """Email notification model. Only handle the sending process, the build process has
    to be implemented by the children class."""

    class Meta:
        verbose_name = _("Email notification")
        proxy = True

    def build(self, person, content):
        raise NotImplementedError(
            "Implement this method to build the notification content"
        )

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

    def process(self):
        """Process the notification by sending the email."""

        email_message = email.message_from_string(self.payload)
        for mail_sender_class in settings.MAIL_SENDER_CLASSES:
            MailSenderClass = import_string(mail_sender_class)
            mail_sender = MailSenderClass(
                receivers=self.person.email,
                reference=None,
                connected_user=None,
                subject=unescape(strip_tags(email_message.get("subject"))),
                message=unescape(strip_tags(email_message.get("body"))),
                html_message=None,
                from_email=settings.DEFAULT_FROM_EMAIL,
                attachment=None,
                cc=None,
            )
            mail_sender.send_mail()
