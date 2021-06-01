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

An email notification is an email message that will be sent to the user once processed.

To be sent, an EmailNotification will need an EmailMessage. You can chose de build it on your own, using osis-mail-template for example. Or you can choose to use the handler to build it for you.

### Build an EmailMessage and create an EmailNotification

Initialize an object describing the notification you want to send : 

```python
from osis_notification.contrib.notification import EmailNotification

recipient = Person.objects.get(user__username="jmr")
language = recipient.language
tokens = {"token_example": "value of the token example"}
subject = "Notification subject"
plain_text_content = "Plain text content"
html_content = "<b>html</b> <i>content</i>"
notification = EmailNotification(
    recipient=recipient,
    subject=subject,
    plain_text_content=plain_text_content,
    html_content=html_content,
)
```
Use this object to build the EmailMessage and create the EmailNotification :
```python
from osis_notification.contrib.handlers import EmailNotificationHandler

# Build the EmailMessage 
email_message = EmailNotificationHandler.build(notification)
# And finally create the EmailNotification
email_notification = EmailNotificationHandler.create(email_message)
```

#### An example using osis_mail_template

```python
from osis_notification.contrib.handlers import EmailNotificationHandler

recipient = Person.objects.get(user__username="jmr")
language = recipient.language
tokens = {"username": person.user.username}
email_message = generate_email(your_mail_template_id, language, tokens, recipients=[recipient])
email_notification = EmailNotificationHandler.create(email_message)
```

Then you have to give the objet to the EmailNotificationHandler :

```python
from osis_notification.contrib.handlers import EmailNotificationHandler

EmailNotificationHandler.create(email_notification)
```

This mail notification will automatically be send by the task runner.

## How notifications are sent?

`osis_notification` is using Celery tasks to send notifications. Those tasks will call Django command to send both web and email notifications.

You can call those commands this way :
```python
from django.core.management import call_command

call_command("send_email_notifications")
call_command("send_web_notifications")
```

The commands are calling the `process` function on their respective handlers for each notification that are found in the DB with the "Pending" state.
