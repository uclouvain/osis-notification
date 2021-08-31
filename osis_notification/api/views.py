from collections import OrderedDict

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from osis_notification.api.serializers import WebNotificationSerializer
from osis_notification.contrib.handlers import WebNotificationHandler
from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SentNotificationListView(generics.ListAPIView):
    """Return all sent notifications associated to a specific user."""

    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    authentication_classes = (SessionAuthentication,)

    def get_paginated_response(self, data):
        unread_count = (
            self.get_queryset().filter(state=NotificationStates.SENT_STATE.name).count()
        )
        return Response(OrderedDict([
            ("count", self.paginator.count),
            ("unread_count", unread_count),
            ("next", self.paginator.get_next_link()),
            ("previous", self.paginator.get_previous_link()),
            ("results", data),
        ]))

    def get_queryset(self):
        return WebNotification.objects.sent().filter(
            person__uuid=self.request.user.person.uuid
        )


class MarkNotificationAsReadView(generics.UpdateAPIView):
    """Mark a single given notification as read if the notification is sent. If the
    notification is already mark as sent, it marks it as sent."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get_object(self):
        return get_object_or_404(
            self.queryset,
            person__uuid=self.request.user.person.uuid,
            uuid=self.kwargs["notification_uuid"],
        )

    def update(self, request, *args, **kwargs):
        WebNotificationHandler.toggle_state(self.get_object())
        return super().update(request, *args, **kwargs)


class MarkAllNotificationsAsReadView(views.APIView):
    """Mark all the current user sent notifications as read."""

    queryset = WebNotification.objects.sent()
    serializer_class = WebNotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(
            state=NotificationStates.SENT_STATE.name,
            person__uuid=self.request.user.person.uuid,
        )

    def put(self, request, *args, **kwargs):
        marked_as_read_notifications = []
        for notification in self.get_queryset():
            WebNotificationHandler.mark_as_read(notification)
            marked_as_read_notifications.append(notification)
        serializer = self.serializer_class(marked_as_read_notifications, many=True)
        return Response(serializer.data)
