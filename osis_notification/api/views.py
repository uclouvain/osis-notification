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

from collections import OrderedDict

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from osis_notification.api.serializers import WebNotificationSerializer
from osis_notification.api.utils import CorsAllowOriginMixin
from osis_notification.contrib.handlers import WebNotificationHandler
from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates


class NotificationPagination(LimitOffsetPagination):
    default_limit = 15

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)

        # Use a single queryset for both counts
        count_queryset = (
            WebNotification.objects.sent()
            .filter(person_id=request.user.person.pk)
            .values('person_id')
            .annotate(
                count=Count('id'),
                unread_count=Count('id', filter=Q(state=NotificationStates.SENT_STATE.name)),
            )
            .order_by()
            .values('count', 'unread_count')
        )
        self.unread_count = 0
        self.count = 0
        if count_queryset:
            self.unread_count = count_queryset[0]['unread_count']
            self.count = count_queryset[0]['count']

        self.offset = self.get_offset(request)
        self.request = request

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("unread_count", self.unread_count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class SentNotificationListView(CorsAllowOriginMixin, generics.ListAPIView):
    """Return all sent notifications associated to a specific user."""

    name = "notification-list"
    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = NotificationPagination
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [SessionAuthentication]

    def get_queryset(self):
        return WebNotification.objects.sent().filter(person_id=self.request.user.person.pk)


class MarkNotificationAsReadView(CorsAllowOriginMixin, generics.UpdateAPIView):
    """Mark a single given notification as read if the notification is sent. If the
    notification is already mark as sent, it marks it as sent."""

    name = "notification-mark-as-read"
    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [SessionAuthentication]

    def get_object(self):
        return get_object_or_404(
            self.queryset,
            person__uuid=self.request.user.person.uuid,
            uuid=self.kwargs["notification_uuid"],
        )

    def perform_update(self, serializer):
        WebNotificationHandler.toggle_state(serializer.instance)


class MarkAllNotificationsAsReadView(CorsAllowOriginMixin, views.APIView):
    """Mark all the current user sent notifications as read."""

    name = "notification-mark-all-as-read"
    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(
            state=NotificationStates.SENT_STATE.name,
            person__uuid=self.request.user.person.uuid,
        )

    def put(self, request, *args, **kwargs):
        notifications = list(self.get_queryset())
        WebNotificationHandler.mark_all_as_read(notifications)
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data)
