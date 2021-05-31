from django.core.management import call_command

from backoffice.celery import app as celery_app


@celery_app.task
def run():
    """This job will launch the Django command that will send all the pending
    notifications."""

    call_command("send_notifications")
