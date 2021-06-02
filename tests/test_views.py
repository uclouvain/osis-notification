from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.tests.factories.person import PersonFactory
from osis_notification.models.enums import NotificationStates
from osis_notification.tests.factories import WebNotificationFactory


class SentNotificationListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.web_notification = WebNotificationFactory(person=cls.person)
        cls.url = reverse(
            "osis_notification:notification-list",
            kwargs={"uuid": cls.person.uuid},
        )

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_view_allows_user_to_retrieve_his_notifications(self):
        # similar to the test in the `test_permissions` file, but with the response here
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_disallows_user_to_see_others_users_notifications(self):
        # similar to the test in the `test_permissions` file, but with the response here
        response = self.client.get(
            reverse(
                "osis_notification:notification-list",
                kwargs={"uuid": PersonFactory().uuid},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_is_only_returning_users_sent_notifications(self):
        response = self.client.get(self.url)
        # As the notification has not yet been sent, we should not retrieve it
        self.assertEqual(response.data["count"], 0)
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 1)

    def test_view_is_only_returning_users_notifications(self):
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
