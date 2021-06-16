from django.core.management.base import BaseCommand

from osis_notification.contrib.handlers import WebNotificationHandler
from osis_notification.models import WebNotification
from osis_notification.signals import web_notification_sent


class Command(BaseCommand):
    help = "Send all the web notifications."

    def handle(self, *args, **options):
        for notification in WebNotification.objects.pending():
            WebNotificationHandler.process(notification)
            web_notification_sent.send(
                sender=self.__class__,
                notification_uuid=notification.uuid,
            )
