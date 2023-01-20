# ##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2023 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
# ##############################################################################

from django.test import override_settings
from django.shortcuts import resolve_url
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from base.tests.factories.person import PersonFactory
from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates
from osis_notification.tests.factories import WebNotificationFactory


class NotificationTestCase(APITestCase):
    def assertNumQueries(self, num, func=None, *args, **kwargs):
        # 2 being SAVEPOINT and RELEASE SAVEPOINT
        return super().assertNumQueries(num + 2, func, *args, **kwargs)


@override_settings(ROOT_URLCONF="osis_notification.api.urls_v1")
class SentNotificationListViewTest(NotificationTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.web_notification = WebNotificationFactory(person=cls.person)
        cls.url = resolve_url("notification-list")

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_allow_user_to_retrieve_his_notifications(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_return_users_sent_notifications(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        # As the notification has not yet been sent, we should not retrieve it
        self.assertEqual(response.json()["count"], 0)
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        self.assertEqual(response.json()["count"], 1)

    def test_only_return_users_notifications(self):
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        web_notification = WebNotificationFactory(person=self.person)
        web_notification.state = NotificationStates.SENT_STATE.name
        web_notification.save()
        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        self.assertEqual(response.json()["count"], 2)
        WebNotificationFactory()
        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        # the result should be the same as the notification is for another person
        self.assertEqual(response.json()["count"], 2)


@override_settings(ROOT_URLCONF="osis_notification.api.urls_v1")
class MarkNotificationAsReadViewTest(NotificationTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = PersonFactory()
        cls.web_notification = WebNotificationFactory(person=cls.person)
        cls.url = resolve_url("notification-mark-as-read", notification_uuid=cls.web_notification.uuid)

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_mark_as_read_a_notification_that_is_not_sent_raises_a_404(self):
        with self.assertNumQueries(2):
            response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_allow_user_to_mark_his_notification_as_read(self):
        self.web_notification.state = NotificationStates.SENT_STATE.name
        self.web_notification.save()
        self.assertIsNone(self.web_notification.read_at)
        with self.assertNumQueries(2):
            response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["state"], NotificationStates.READ_STATE.name)
        self.assertIsNotNone(response.json()["read_at"])

    def test_allow_user_to_mark_his_notification_as_unread(self):
        self.web_notification.state = NotificationStates.READ_STATE.name
        self.web_notification.read_at = now()
        self.web_notification.save()
        with self.assertNumQueries(2):
            response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["state"], NotificationStates.SENT_STATE.name)
        self.assertIsNone(response.json()["read_at"])

    def test_disallow_user_to_mark_others_users_notification_as_read(self):
        person = PersonFactory()
        web_notification = WebNotificationFactory(person=person)
        with self.assertNumQueries(2):
            response = self.client.patch(resolve_url("notification-mark-as-read", notification_uuid=web_notification.uuid))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(ROOT_URLCONF="osis_notification.api.urls_v1")
class MarkAllNotificationsAsReadViewTest(NotificationTestCase):
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
        cls.url = resolve_url("notification-mark-all-as-read")

    def setUp(self):
        self.client.force_authenticate(user=self.person.user)

    def test_allow_user_to_mark_all_his_notifications_as_read(self):
        self.assertEqual(
            WebNotification.objects.filter(state=NotificationStates.SENT_STATE.name).count(),
            self.sent_notification_count,
        )
        with self.assertNumQueries(2):
            response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            WebNotification.objects.filter(state=NotificationStates.READ_STATE.name).count(),
            self.sent_notification_count,
        )
