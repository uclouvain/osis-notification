# OSIS Notification

`OSIS Notification` is a Django application to manage notifications sending across OSIS plateform.


Requirements
===========

`OSIS Notification` requires

- Django 2.2+
- Django REST Framework 3.12+
- Celery 4+
- Vue 3

# How to install ?

## Configuring Django

Add `osis_notification` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'osis_notification',
    ...
)
```

# Using OSIS Notification

`osis_notification` provides an API to create and send notifications and also a VueJS component to view them in the interface.

## Web notification

A web notification is a simple text that will be shown to the user on the web interface.

### Create and send

To create it, you must implement the `build` method from the abstract class `WebNotification` :

```python
from osis_notification.models import WebNotification

class AdmissionSendWebNotification(WebNotification):
    def build(person, admission_notification_content):
         content = f"hello {person}, you have a new message about your admission : {admission_notification_content}"
         super().create(person, content)
```

This web notification will automatically be send by the task runner.

## Email notification

An email notification is a email message that will be sent to the user once processed.

### Create and send

To create it, you must implement the `build` method from the abstract class `MailNotification` :

```python
from osis_notification.models import MailNotification

class AdmissionSendMailNotification(MailNotification):
    def build(person, doctorate_request):
         subject, content = render_email_content(NEW_ADMISSION_TEMPLATE, person.language, **tokens)
         super().create(person, content)
```

This mail notification will automatically be send by the task runner.
