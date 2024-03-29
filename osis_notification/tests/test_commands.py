from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.test import override_settings
from django.utils.timezone import now

from base.tests.factories.person import PersonFactory
from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.contrib.notification import (
    EmailNotification as EmailNotificationType,
)
from osis_notification.contrib.exceptions import EmailNotificationSendingException
from osis_notification.models import EmailNotification, WebNotification, Notification
from osis_notification.models.enums import NotificationStates
from osis_notification.tests import TestCase
from osis_notification.tests.factories import (
    EmailNotificationFactory,
    WebNotificationFactory,
)

from osis_common.messaging.mail_sender_classes import MessageHistorySender


class SendNotificationsTest(TestCase):
    def setUp(self):
        self.web_notification = WebNotificationFactory()
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
        self.email_notification = EmailNotificationFactory(
            payload=email_message.as_string(),
            person=email_notification_data["recipient"],
        )

    def test_send_email_notifications(self):
        # ensure email notification is in pending state after creation
        self.assertEqual(
            self.email_notification.state,
            NotificationStates.PENDING_STATE.name,
        )
        with self.assertNumQueriesLessThan(6):
            call_command("send_email_notifications")
        self.email_notification.refresh_from_db()
        # now email notification should be in sent state
        self.assertEqual(
            self.email_notification.state,
            NotificationStates.SENT_STATE.name,
        )

    def test_send_email_notifications_with_failure(self):
        second_email_notification = EmailNotificationFactory(
            payload=self.email_notification.payload,
            person=self.email_notification.person,
        )
        third_email_notification = EmailNotificationFactory(
            payload=self.email_notification.payload,
            person=self.email_notification.person,
        )

        original_send_mail = Notification.save
        with patch.object(Notification, 'save') as sender_mock:
            sender_mock.side_effect = [original_send_mail, ValueError('Invalid value'), Exception('Custom error')]

            with self.assertRaisesRegex(
                EmailNotificationSendingException,
                f'Errors occurred while sending the email notifications:'
                f'\n{second_email_notification.uuid}: Invalid value.'
                f'\n{third_email_notification.uuid}: Custom error.'
            ):
                call_command("send_email_notifications")

                self.email_notification.refresh_from_db()
                self.assertEqual(self.email_notification.state, NotificationStates.SENT_STATE.name)

                second_email_notification.refresh_from_db()
                self.assertEqual(second_email_notification.state, NotificationStates.PENDING_STATE.name)

                third_email_notification.refresh_from_db()
                self.assertEqual(second_email_notification.state, NotificationStates.PENDING_STATE.name)


    def test_send_web_notifications(self):
        # ensure web notification is in pending state after creation
        self.assertEqual(
            self.web_notification.state,
            NotificationStates.PENDING_STATE.name,
        )
        with self.assertNumQueriesLessThan(3):
            call_command("send_web_notifications")
        self.web_notification.refresh_from_db()
        # now web notification should be in sent state
        self.assertEqual(
            self.web_notification.state,
            NotificationStates.SENT_STATE.name,
        )


@override_settings(WEB_NOTIFICATIONS_RETENTION_DAYS=10)
class CleanWebNotificationsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a notification with read_at field older than defined retention duration
        read_at = now() - timedelta(days=settings.WEB_NOTIFICATIONS_RETENTION_DAYS)
        old_web_notification = WebNotificationFactory()
        old_web_notification.read_at = read_at + timedelta(days=1)
        old_web_notification.state = NotificationStates.READ_STATE.name
        old_web_notification.save()
        # Create a notification with read_at field still in defined retention duration
        web_notification = WebNotificationFactory()
        web_notification.read_at = read_at
        web_notification.state = NotificationStates.READ_STATE.name
        web_notification.save()

    def test_clean_email_notifications_removes_only_old_notifications_in_db(self):
        self.assertEqual(WebNotification.objects.count(), 2)
        call_command("clean_web_notifications")
        self.assertEqual(WebNotification.objects.count(), 1)


@override_settings(EMAIL_NOTIFICATIONS_RETENTION_DAYS=10)
class CleanEmailNotificationsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a notification with read_at field older than defined retention duration
        sent_at = now() - timedelta(days=settings.EMAIL_NOTIFICATIONS_RETENTION_DAYS)
        old_email_notification = EmailNotificationFactory(payload="test payload")
        old_email_notification.sent_at = sent_at + timedelta(days=1)
        old_email_notification.state = NotificationStates.SENT_STATE.name
        old_email_notification.save()
        # Create a notification with sent_at field still in defined retention duration
        email_notification = EmailNotificationFactory(payload="test payload")
        email_notification.sent_at = sent_at
        email_notification.state = NotificationStates.SENT_STATE.name
        email_notification.save()

    def test_clean_email_notifications_removes_only_old_notifications_in_db(self):
        self.assertEqual(EmailNotification.objects.count(), 2)
        call_command("clean_email_notifications")
        self.assertEqual(EmailNotification.objects.count(), 1)
