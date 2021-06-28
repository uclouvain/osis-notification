from django.dispatch import Signal


email_notification_sent = Signal(providing_args=["notification"])
