import email
from html import unescape

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.timezone import now

from osis_notification.models import EmailNotification as EmailNotificationModel
from osis_notification.models.enums import NotificationStates


class EmailNotification:
    """Email notification class. Only handle the sending process, the build process has
    to be implemented by the children class."""

    def build(self, person, content):
        raise NotImplementedError(
            "Implement this method to build the notification content"
        )

    @staticmethod
    def process(notification: EmailNotificationModel):
        """Process the notification by sending the email."""

        email_message = email.message_from_string(notification.payload)
        for mail_sender_class in settings.MAIL_SENDER_CLASSES:
            MailSenderClass = import_string(mail_sender_class)
            mail_sender = MailSenderClass(
                receivers=notification.person.email,
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
        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_datetime = now()
        notification.save()
