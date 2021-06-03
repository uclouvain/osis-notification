from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from base.tests.factories.person import PersonFactory
from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates
from osis_notification.tests.factories import WebNotificationFactory


class SentNotificationListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.web_notification = WebNotificationFactory(person=cls.person)
        cls.url = reverse("osis_notification:notification-list")

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_allow_user_to_retrieve_his_notifications(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_return_users_sent_notifications(self):
        response = self.client.get(self.url)
        # As the notification has not yet been sent, we should not retrieve it
        self.assertEqual(response.data["count"], 0)
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 1)

    def test_only_return_users_notifications(self):
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        web_notification = WebNotificationFactory(person=self.person)
        web_notification.state = NotificationStates.SENT_STATE.name
        web_notification.save()
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 2)
        WebNotificationFactory()
        response = self.client.get(self.url)
        # the result should be the same as the notification is for an other person
        self.assertEqual(response.data["count"], 2)


class MarkNotificationAsReadViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.web_notification = WebNotificationFactory(person=cls.person)
        cls.url = reverse(
            "osis_notification:notification-mark-as-read",
            kwargs={"notification_uuid": cls.web_notification.uuid},
        )

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_mark_as_read_a_notification_that_is_not_sent_raises_a_404(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_allow_user_to_mark_his_notification_as_read(self):
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        self.assertIsNone(self.web_notification.read_at)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["state"], NotificationStates.READ_STATE.name)
        self.assertIsNotNone(response.data["read_at"])

    def test_allow_user_to_mark_his_notification_as_unread(self):
        self.web_notification.state = NotificationStates.READ_STATE.name
        self.web_notification.read_at = now()
        self.web_notification.save()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["state"], NotificationStates.SENT_STATE.name)
        self.assertIsNone(response.data["read_at"])

    def test_disallow_user_to_mark_others_users_notification_as_read(self):
        person = PersonFactory()
        web_notification = WebNotificationFactory(person=person)
        response = self.client.patch(
            reverse(
                "osis_notification:notification-mark-as-read",
                kwargs={"notification_uuid": web_notification.uuid},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MarkAllNotificationsAsReadViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        # create several notifications with SENT status
        cls.sent_notification_count = 10
        for _ in range(cls.sent_notification_count):
            web_notification = WebNotificationFactory(person=cls.person)
            web_notification.state = NotificationStates.SENT_STATE.name
            web_notification.sent_at = now()
            web_notification.save()
        cls.url = reverse("osis_notification:notification-mark-all-as-read")

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_allow_user_to_mark_all_his_notifications_as_read(self):
        self.assertEqual(
            WebNotification.objects.filter(
                state=NotificationStates.SENT_STATE.name
            ).count(),
            self.sent_notification_count,
        )
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            WebNotification.objects.filter(
                state=NotificationStates.READ_STATE.name
            ).count(),
            self.sent_notification_count,
        )
