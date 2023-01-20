# ##############################################################################
#
#  OSIS stands for Open Student Information System. It's an application
#  designed to manage the core business of higher education institutions,
#  such as universities, faculties, institutes and professional schools.
#  The core business involves the administration of students, teachers,
#  courses, programs and so on.
#
#  Copyright (C) 2015-2023 Université catholique de Louvain (http://www.uclouvain.be)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  A copy of this license - GNU General Public License - is available
#  at the root of the source code of this program.  If not,
#  see http://www.gnu.org/licenses/.
#
# ##############################################################################

import email
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.policy import default as default_policy
from html import unescape
from typing import List, Optional

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
        """Build an EmailMessage object from a EmailNotification object.

        :param notification: An EmailNotification object describing the email
            notification to be sent
        :return: The built EmailMessage."""

        mail = EmailMessage(policy=default_policy)
        mail.set_charset(settings.DEFAULT_CHARSET)
        # Set plain text content
        mail.set_content(notification.plain_text_content)
        # Set html content
        mail.add_alternative(notification.html_content, subtype="html")
        mail["Subject"] = notification.subject
        mail["From"] = settings.DEFAULT_FROM_EMAIL
        mail["To"] = (
            notification.recipient.email if isinstance(notification.recipient, Person) else notification.recipient
        )

        return mail

    @staticmethod
    def create(
        mail: EmailMessage,
        person: Optional[Person] = None,
    ) -> EmailNotification:
        """Create an email notification from a python object and save it in the database.

        :param mail: The email message to be sent as a notification.
        :param person: The recipient of the notification.
        :return: The created EmailNotification."""

        if person is None:
            person = Person.objects.filter(email=mail["To"]).first()

        return EmailNotification.objects.create(
            person=person,
            payload=str(mail),
        )

    @staticmethod
    def process(notification: EmailNotification):
        """Process the notification by sending the email.

        :param notification: The notification to be sent."""

        email_message = email.message_from_string(notification.payload, policy=default_policy)
        receiver = create_receiver(
            notification.person_id,
            email_message.get("to"),
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

    @staticmethod
    def mark_all_as_read(notifications: List["WebNotification"]):
        for notification in notifications:
            notification.state = NotificationStates.READ_STATE.name
            notification.read_at = now()

        WebNotification.objects.bulk_update(notifications, ["state", "read_at"])
