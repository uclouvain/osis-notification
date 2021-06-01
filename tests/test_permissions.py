from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from base.tests.factories.person import PersonFactory
from osis_notification.api.permissions import IsNotificationRecipient
from osis_notification.api.views import SentNotificationListView


class IsNotificationRecipientTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.url = reverse(
            "osis_notification:notification-list",
            kwargs={"uuid": cls.person.uuid},
        )
        cls.permission = IsNotificationRecipient()
        cls.factory = APIRequestFactory()
        cls.view = SentNotificationListView(kwargs={"uuid": cls.person.uuid})

    def test_permission_allows_user_to_retrieve_his_notifications(self):
        request = self.factory.get(self.url)
        request.user = self.person.user
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_permission_disallows_user_to_see_others_users_notifications(self):
        request = self.factory.get(self.url)
        request.user = PersonFactory().user
        self.assertFalse(self.permission.has_permission(request, self.view))
