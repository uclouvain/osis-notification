import email
from email.message import EmailMessage
from html import unescape
from typing import Type

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.timezone import now

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
        mail.set_content(notification.content)
        mail["Subject"] = "To define"  # TODO define this
        mail["From"] = settings.DEFAULT_FROM_EMAIL
        mail["To"] = notification.recipient.user.email

        EmailNotification.objects.create(
            person=notification.recipient,
            payload=mail.as_string(),
        )

    @staticmethod
    def process(notification):
        """Process the notification by sending the email.

        :param notification: The notification to be send."""

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
    def process(notification):
        """Process the notification by sending the web notification."""

        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_datetime = now()
        notification.save()
