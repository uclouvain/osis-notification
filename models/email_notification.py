import email
from html import unescape

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _

from osis_notification.models import Notification
from osis_notification.models.enums import NotificationTypes


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
