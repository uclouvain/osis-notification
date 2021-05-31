from django.core.management.base import BaseCommand

from osis_notification.contrib.handlers import (
    EmailNotificationHandler,
    WebNotificationHandler,
)
from osis_notification.models import EmailNotification, WebNotification


class Command(BaseCommand):
    help = "Send all the notifications."

    def handle(self, *args, **options):
        for notification in EmailNotification.objects.pending():
            EmailNotificationHandler.process(notification)
        for notification in WebNotification.objects.pending():
            WebNotificationHandler.process(notification)
