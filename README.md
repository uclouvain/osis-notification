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

Initialize an object describing the notification you want to send : 

```python
from osis_notification.contrib.notification import WebNotification

recipient = Person.objects.get(user__username="jmr")
content = "This is the content of the web notification"
web_notification = WebNotification(recipient=recipient, content=content)
```

Then you have to give the objet to the WebNotificationHandler :

```python
from osis_notification.contrib.handlers import WebNotificationHandler

WebNotificationHandler.create(web_notification)
```

This web notification will automatically be send by the task runner.

## Email notification

An email notification is a email message that will be sent to the user once processed.

### Create and send

Initialize an object describing the notification you want to send : 

```python
from osis_notification.contrib.notification import EmailNotification

recipient = Person.objects.get(user__username="jmr")
content = "This is the content of the email notification"
email_notification = EmailNotification(recipient=recipient, content=content)
```

Then you have to give the objet to the EmailNotificationHandler :

```python
from osis_notification.contrib.handlers import EmailNotificationHandler

EmailNotificationHandler.create(email_notification)
```

This mail notification will automatically be send by the task runner.
