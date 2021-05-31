import mock
from django.test import TestCase

from base.tests.factories.person import PersonFactory
from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
)
from osis_notification.tasks import notification_sender
from osis_notification.tests.factories import (
    EmailNotificationFactory,
    WebNotificationFactory,
)


class TestNotificationSenderTask(TestCase):

    @mock.patch("osis_notification.management.commands.send_notifications.Command")
    def test_send_web_notification(self, mock_send_notification):
        WebNotificationFactory()
        notification_sender.run()
        self.assertTrue(mock_send_notification.called)

    @mock.patch("osis_notification.management.commands.send_notifications.Command")
    def test_send_email_notification(self, mock_send_notification):
        email_notification_data = {
            "recipient": PersonFactory(),
            "subject": "Email notification test subject",
            "plain_text_content": "Email notification test content as plain text",
            "html_content": "<b>Email notification</b> test content as <i>html</i>",
        }
        email_notification = EmailNotificationType(**email_notification_data)
        email_message = EmailNotificationHandler.build(email_notification)
        EmailNotificationFactory(
            payload=email_message.as_string(),
            person=email_notification_data["recipient"],
        )
        notification_sender.run()
        self.assertTrue(mock_send_notification.called)
