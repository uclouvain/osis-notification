from django.urls import path

from osis_notification.api.views import SentNotificationListView

app_name = "osis_notification"
urlpatterns = [
    path("<uuid:uuid>/", SentNotificationListView.as_view(), name="notification-list"),
]
