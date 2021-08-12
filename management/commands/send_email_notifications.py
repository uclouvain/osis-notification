from django.core.management.base import BaseCommand

from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.models import EmailNotification


class Command(BaseCommand):
    help = "Send all the email notifications."

    def handle(self, *args, **options):
        for notification in EmailNotification.objects.pending():
            EmailNotificationHandler.process(notification)
