from django.dispatch import Signal


web_notification_sent = Signal(providing_args=["notification_uuid"])
