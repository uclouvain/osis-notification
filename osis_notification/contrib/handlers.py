import email
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.policy import default as default_policy
from html import unescape
from typing import Optional

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.timezone import now

from base.models.person import Person
from osis_common.messaging.message_config import create_receiver
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
    WebNotification as WebNotificationType,
)
from osis_notification.models import EmailNotification, WebNotification
from osis_notification.models.enums import NotificationStates


class EmailNotificationHandler:
    @staticmethod
    def build(notification: EmailNotificationType) -> EmailMessage:
        """Build a EmailMessage object from a EmailNotification object.

        :param notification: A EmailNotification object describing the email
            notification to be send
        :return: The built EmailMessage."""

        mail = EmailMessage(policy=default_policy)
        mail.set_charset(settings.DEFAULT_CHARSET)
        # Set plain text content
        mail.set_content(notification.plain_text_content)
        # Set html content
        mail.add_alternative(notification.html_content, subtype="html")
        mail["Subject"] = notification.subject
        mail["From"] = settings.DEFAULT_FROM_EMAIL
        mail["To"] = notification.recipient.email

        return mail

    @staticmethod
    def create(
        mail: EmailMessage,
        person: Optional[Person] = None,
    ) -> EmailNotification:
        """Create an email notification from a python object and save it in the database.

        :param mail: The email message to be send as a notification.
        :param person: The recipient of the notification.
        :return: The created EmailNotification."""

        if person is None:
            person = Person.objects.get(email=mail["To"])

        return EmailNotification.objects.create(
            person=person,
            payload=str(mail),
        )

    @staticmethod
    def process(notification: EmailNotification):
        """Process the notification by sending the email.

        :param notification: The notification to be send."""

        email_message = email.message_from_string(notification.payload, policy=default_policy)
        receiver = create_receiver(
            notification.person.id,
            notification.person.email,
            settings.LANGUAGE_CODE,
        )
        plain_text_content = ''
        html_content = ''
        for part in email_message.walk():
            # Mail payload is decoded to bytes then decode to utf8
            if part.get_content_type() == "text/plain":
                plain_text_content = part.get_payload(decode=True).decode(settings.DEFAULT_CHARSET)
            elif part.get_content_type() == "text/html":
                html_content = part.get_payload(decode=True).decode(settings.DEFAULT_CHARSET)

        subject = make_header(decode_header(email_message.get("subject")))
        cc = email_message.get("Cc")
        if cc:
            cc = [Person(email=cc_email) for cc_email in cc.split(',')]
        for mail_sender_class in settings.MAIL_SENDER_CLASSES:
            MailSenderClass = import_string(mail_sender_class)
            mail_sender = MailSenderClass(
                receivers=[receiver],
                reference=None,
                connected_user=None,
                subject=unescape(strip_tags(str(subject))),
                message=plain_text_content.rstrip(),
                html_message=html_content.rstrip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                attachment=None,
                cc=cc,
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

    @staticmethod
    def toggle_state(notification: WebNotification):
        """Toggle the notification state between `SENT_STATE` and `READ_STATE`."""

        if notification.state == NotificationStates.READ_STATE.name:
            notification.state = NotificationStates.SENT_STATE.name
            notification.read_at = None
        else:
            notification.state = NotificationStates.READ_STATE.name
            notification.read_at = now()
        notification.save()

    @staticmethod
    def mark_as_read(notification: WebNotification):
        notification.state = NotificationStates.READ_STATE.name
        notification.read_at = now()
        notification.save()
