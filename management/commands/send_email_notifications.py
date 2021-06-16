from django.core.management.base import BaseCommand

from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.models import EmailNotification
from osis_notification.signals import email_notification_sent


class Command(BaseCommand):
    help = "Send all the email notifications."

    def handle(self, *args, **options):
        for notification in EmailNotification.objects.pending():
            EmailNotificationHandler.process(notification)
            email_notification_sent.send(
                sender=self.__class__,
                notification_uuid=notification.uuid,
            )
