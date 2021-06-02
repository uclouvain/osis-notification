from django.core.management import call_command

from base.tests.factories.person import PersonFactory
from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
)
from osis_notification.models.enums import NotificationStates
from osis_notification.tests import TestCase
from osis_notification.tests.factories import (
    EmailNotificationFactory,
    WebNotificationFactory,
)


class SendNotificationsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.web_notification = WebNotificationFactory()
        # It's seems a bit more complicated to create the email message payload in a
        # factory so I leave it like this for the moment
        email_notification_data = {
            "recipient": PersonFactory(),
            "subject": "Email notification test subject",
            "plain_text_content": "Email notification test content as plain text",
            "html_content": "<b>Email notification</b> test content as <i>html</i>",
        }
        email_notification = EmailNotificationType(**email_notification_data)
        email_message = EmailNotificationHandler.build(email_notification)
        cls.email_notification = EmailNotificationFactory(
            payload=email_message.as_string(),
            person=email_notification_data["recipient"],
        )

    def test_send_email_notifications(self):
        # ensure email notification is in pending state after creation
        self.assertEqual(
            self.email_notification.state, NotificationStates.PENDING_STATE.name
        )
        with self.assertNumQueriesLessThan(6):
            call_command("send_email_notifications")
        self.email_notification.refresh_from_db()
        # now email notification should be in sent state
        self.assertEqual(
            self.email_notification.state, NotificationStates.SENT_STATE.name
        )

    def test_send_web_notifications(self):
        # ensure web notification is in pending state after creation
        self.assertEqual(
            self.web_notification.state, NotificationStates.PENDING_STATE.name
        )
        with self.assertNumQueriesLessThan(3):
            call_command("send_web_notifications")
        self.web_notification.refresh_from_db()
        # now web notification should be in sent state
        self.assertEqual(
            self.web_notification.state, NotificationStates.SENT_STATE.name
        )
