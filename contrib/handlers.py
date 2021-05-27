import email
from email.message import EmailMessage
from html import unescape

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.timezone import now

from osis_common.messaging.message_config import create_receiver
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
    WebNotification as WebNotificationType,
)
from osis_notification.models import EmailNotification, WebNotification
from osis_notification.models.enums import NotificationStates


class EmailNotificationHandler:

    @staticmethod
    def create(notification: EmailNotificationType):
        """Create a email notification from a python object and save it in the database.

        :param notification: An object containing the notification's content and the
            person to send it to."""

        mail = EmailMessage()
        # Set plain text content
        mail.set_content(notification.plain_text_content)
        # Set html content
        mail.add_alternative(notification.html_content, subtype="html")
        mail["Subject"] = notification.subject
        mail["From"] = settings.DEFAULT_FROM_EMAIL
        mail["To"] = notification.recipient.user.email

        return EmailNotification.objects.create(
            person=notification.recipient,
            payload=mail.as_string(),
        )

    @staticmethod
    def process(notification: EmailNotification):
        """Process the notification by sending the email.

        :param notification: The notification to be send."""

        email_message = email.message_from_string(notification.payload)
        receiver = create_receiver(
            notification.person.id,
            notification.person.user.email,
            settings.LANGUAGE_CODE,
        )
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                plain_text_content = part.get_payload()
            elif part.get_content_type() == "text/html":
                html_content = part.get_payload()

        for mail_sender_class in settings.MAIL_SENDER_CLASSES:
            MailSenderClass = import_string(mail_sender_class)
            mail_sender = MailSenderClass(
                receivers=[receiver],
                reference=None,
                connected_user=None,
                subject=unescape(strip_tags(email_message.get("subject"))),
                message=plain_text_content,
                html_message=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                attachment=None,
                cc=None,
            )
            mail_sender.send_mail()
        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_at = now()
        notification.save()


class WebNotificationHandler:

    @staticmethod
    def create(notification: WebNotificationType):
        """Create a web notification from a python object and save it in the database.

        :param notification: An object containing the notification's content and the
            person to send it to."""

        return WebNotification.objects.create(
            person=notification.recipient,
            payload=notification.content,
        )

    @staticmethod
    def process(notification: WebNotification):
        """Process the notification by sending the web notification."""

        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_at = now()
        notification.save()
