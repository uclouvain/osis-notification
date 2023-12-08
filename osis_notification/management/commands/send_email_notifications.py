from django.core.management.base import BaseCommand

from osis_notification.contrib.handlers import EmailNotificationHandler
from osis_notification.contrib.exceptions import EmailNotificationSendingException
from osis_notification.models import EmailNotification


class Command(BaseCommand):
    help = "Send all the email notifications."

    def handle(self, *args, **options):
        exceptions = {}

        for notification in EmailNotification.objects.pending():
            try:
                EmailNotificationHandler.process(notification)
            except Exception as exception:
                exceptions[notification.uuid] = exception

        if exceptions:
            raise EmailNotificationSendingException(exceptions)
