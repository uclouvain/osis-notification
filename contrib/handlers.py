import email
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
    """Email notification handler class. Only handle the sending process, the build
    process has to be implemented by the children class."""

    @staticmethod
    def create(notification: Type[EmailNotificationType]):
        # TODO serializer
        # TODO email_message_to_string
        EmailNotification.objects.create(
            person=notification.person,
            content=notification.content,
        )

    @staticmethod
    def process(notification):
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


class WebNotificationHandler:
    """Web notification handler class."""

    @staticmethod
    def create(notification: Type[WebNotificationType]):
        """Create and send the notification.

        :param notification: An object containing the notification's content and the
            person to send it to."""
        return WebNotification.objects.create(
            person=notification.person,
            content=notification.content,
        )

    @staticmethod
    def process(notification_id):
        """Process the notification by sending the web notification."""

        notification = WebNotification.objects.get(id=notification_id)
        notification.state = NotificationStates.SENT_STATE.name
        notification.sent_datetime = now()
        notification.save()
