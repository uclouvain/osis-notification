from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from osis_notification.models import WebNotification
from osis_notification.models.enums import NotificationStates


class Command(BaseCommand):
    help = (
        "Clean all the read web notifications that are older than the defined "
        "retention duration. "
    )

    def handle(self, *args, **options):
        maximum_retention_date = now() - timedelta(
            days=settings.NOTIFICATIONS_RETENTION_DAYS
        )
        WebNotification.objects.filter(
            state=NotificationStates.READ_STATE.name,
            read_at__lte=maximum_retention_date,
        ).delete()
