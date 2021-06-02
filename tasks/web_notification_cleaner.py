from django.core.management import call_command

from backoffice.celery import app as celery_app


@celery_app.task
def run():
    """This job will launch the Django command that will clean all the old web
    notifications."""

    call_command("clean_web_notifications")
