import email

from django.test import TestCase

from base.tests.factories.person import PersonFactory
from osis_common.models import message_history
from osis_notification.contrib.handlers import (
    WebNotificationHandler,
    EmailNotificationHandler,
)
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
    WebNotification as WebNotificationType,
)
from osis_notification.models import WebNotification, EmailNotification
from osis_notification.models.enums import NotificationStates


class HandlersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.web_notification_data = {
            "recipient": PersonFactory(),
            "content": "Web notification test content",
        }
        cls.web_notification = WebNotificationType(**cls.web_notification_data)
        cls.email_notification_data = {
            "recipient": PersonFactory(),
            "subject": "Email notification test subject",
            "plain_text_content": "Email notification test content as plain text",
            "html_content": "<b>Email notification</b> test content as <i>html</i>",
        }
        cls.email_notification = EmailNotificationType(**cls.email_notification_data)

    def test_web_notification_handler_creates_object_with_correct_values(self):
        WebNotificationHandler.create(self.web_notification)
        self.assertEqual(WebNotification.objects.count(), 1)
        web_notification = WebNotification.objects.get()
        self.assertEqual(
            web_notification.person, self.web_notification_data["recipient"]
        )
        self.assertEqual(
            web_notification.payload, self.web_notification_data["content"]
        )

    def test_email_notification_handler_creates_object_with_correct_values(self):
        email_message = EmailNotificationHandler.build(self.email_notification)
        EmailNotificationHandler.create(email_message)
        self.assertEqual(EmailNotification.objects.count(), 1)
        email_notification = EmailNotification.objects.get()
        self.assertEqual(
            email_notification.person, self.email_notification_data["recipient"]
        )
        email_message = email.message_from_string(email_notification.payload)
        self.assertTrue(email_message.is_multipart())
        # Now check the payload of each part (plain text and html)
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                self.assertEqual(
                    part.get_payload().rstrip("\n"),
                    self.email_notification_data["plain_text_content"],
                )
            elif part.get_content_type() == "text/html":
                self.assertEqual(
                    part.get_payload().rstrip("\n"),
                    self.email_notification_data["html_content"],
                )
        self.assertEqual(
            email_message.get("subject"),
            self.email_notification_data["subject"],
        )

    def test_email_notification_handler_process_is_sending_the_email(self):
        self.assertEqual(message_history.MessageHistory.objects.count(), 0)
        email_message = EmailNotificationHandler.build(self.email_notification)
        email_notification = EmailNotificationHandler.create(email_message)
        self.assertEqual(
            email_notification.state, NotificationStates.PENDING_STATE.name
        )
        self.assertIsNone(email_notification.sent_at)
        EmailNotificationHandler.process(email_notification)
        email_notification.refresh_from_db()
        self.assertEqual(message_history.MessageHistory.objects.count(), 1)
        self.assertEqual(email_notification.state, NotificationStates.SENT_STATE.name)
        self.assertIsNotNone(email_notification.sent_at)

    def test_web_notification_handler_process_is_changing_state(self):
        web_notification = WebNotificationHandler.create(self.web_notification)
        self.assertIsNone(web_notification.sent_at)
        self.assertEqual(web_notification.state, NotificationStates.PENDING_STATE.name)
        WebNotificationHandler.process(web_notification)
        web_notification.refresh_from_db()
        self.assertEqual(web_notification.state, NotificationStates.SENT_STATE.name)
        self.assertIsNotNone(web_notification.sent_at)
