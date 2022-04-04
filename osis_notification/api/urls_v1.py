from django.urls import path

from osis_notification.api.views import (
    MarkAllNotificationsAsReadView,
    MarkNotificationAsReadView,
    SentNotificationListView,
)

urlpatterns = [
    path("", SentNotificationListView.as_view(), name="notification-list"),
    path(
        "mark_all_as_read",
        MarkAllNotificationsAsReadView.as_view(),
        name="notification-mark-all-as-read",
    ),
    path(
        "<uuid:notification_uuid>",
        MarkNotificationAsReadView.as_view(),
        name="notification-mark-as-read",
    ),
]
