# OSIS Notification

`OSIS Notification` is a Django application to manage notifications sending across OSIS platform.


Requirements
===========

`OSIS Notification` requires

- Django 2.2+
- Django REST Framework 3.12+
- Vue 3

# How to install ?

## For production

```bash
# From your osis install, with python environment activated
pip install git+https://github.com/uclouvain/osis-notification.git@dev#egg=osis_notification
```

## For development

```bash
# From your osis install, with python environment activated
git clone git@github.com:uclouvain/osis-notification.git
pip install -e ./osis-notification
```


## Configuring Django

Add `osis_notification` to `INSTALLED_APPS` and configure the email and web retention days [see this part](#cleaning-notifications) :

```python
INSTALLED_APPS = (
    ...,
    'osis_notification',
    ...,
)

EMAIL_NOTIFICATIONS_RETENTION_DAYS = 15
WEB_NOTIFICATIONS_RETENTION_DAYS = 30

# The primary server full url (do not set on primary server)
OSIS_NOTIFICATION_BASE_URL = os.environ.get('OSIS_NOTIFICATION_BASE_URL', 'https://yourserver.com/')

# When used on multiple servers, set the domains on which raw files may be displayed (for Content Security Policy)
OSIS_NOTIFICATION_DOMAIN_LIST = [
    '127.0.0.1:8001',
]
```

OSIS-Notification is aimed at being run on multiple servers, so on your primary server, add it to your `urls.py`
matching what you set in `settings.OSIS_NOTIFICATION_BASE_URL`:

```python
if 'osis_notification' in settings.INSTALLED_APPS:
    urlpatterns += (path('osis_notification/', include('osis_notification.api.urls_v1')),)
```

# Using OSIS Notification

`osis_notification` provides an API to create and send notifications and also a VueJS component to view them in the
interface.

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
email_message = generate_email(your_mail_template_id, language, tokens, recipients=[recipient.email])
email_notification = EmailNotificationHandler.create(email_message)
```

Then you have to give the objet to the EmailNotificationHandler :

```python
from osis_notification.contrib.handlers import EmailNotificationHandler

EmailNotificationHandler.create(email_notification)
```

This mail notification will automatically be send by the task runner.

## Sending notification

`osis_notification` is using Celery tasks to send notifications. Those tasks will call Django command to send both web and email notifications.

You can call those commands this way :
```python
from django.core.management import call_command

call_command("send_email_notifications")
call_command("send_web_notifications")
```

The commands are calling the `process` function on their respective handlers for each notification that are found in the DB with the "Pending" state.

## Cleaning notifications

To avoid database overflowing, all the sent email notifications and the read web notifications are deleted after a defined retention duration. You will have to define this duration in your Django settings like this :

```python
EMAIL_NOTIFICATIONS_RETENTION_DAYS = 15
WEB_NOTIFICATIONS_RETENTION_DAYS = 30
```

This duration is set in days.

A Celery task will call a Django command responsible for deleting all the notifications that are older than this duration and have been sent or read :

```python
from django.core.management import call_command

call_command("clean_email_notifications")
call_command("clean_web_notifications")
```

# Integrate the front-end notification component

Make the dependencies available:
```html
<link rel="stylesheet" href="https://unpkg.com/bootstrap@3.3.7/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.5.0/css/all.min.css">
<script type="text/javascript" src="https://unpkg.com/jquery"></script>
<script type="text/javascript" src="https://unpkg.com/bootstrap@3.3.7/dist/js/bootstrap.js"></script>

<link href="{% static 'osis_notification/osis-notification.css' %}" rel="stylesheet"/>
<script src="https://unpkg.com/vue/dist/vue.js"></script>
<script src="https://unpkg.com/vue-i18n@8"></script>

<!-- This line must go at the end of the file -->
<script type="text/javascript" src="{% static 'osis_notification/osis-notification.umd.min.js' %}"></script>

```

Then you can integrate the component:

```html
{% load osis_notification %}{% notification_viewer %}
```

And specify few options by passing them to `notification_viewer` tag:

- `interval` : The interval, in second, to fetch the notifications from the server (default to 300)
- `truncate_length`: number of characters after which the notification is truncated (default is 60)
- `limit`: number of notification to display per page (default is 15)
