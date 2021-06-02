from django.urls import path

from osis_notification.api.views import (
    MarkNotificationAsReadView,
    SentNotificationListView,
)

app_name = "osis_notification"
urlpatterns = [
    path("<uuid:uuid>/", SentNotificationListView.as_view(), name="notification-list"),
    path(
        "<uuid:uuid>/<int:pk>/",
        MarkNotificationAsReadView.as_view(),
        name="notification-mark-as-read",
    ),
]
