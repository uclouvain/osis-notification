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

```
INSTALLED_APPS = (
    ...
    'osis_notification',
    ...
)
```

# Using OSIS Notification

`osis_notification` provides an API to create and send notifications and also a VueJS component to view them in the interface.``

## Creating a web notification

A web notification is a simple text that will be shown to the user on the web interface :

```
from osis_notification import create_web_notification
create_web_notification(    person,    'A signature has been added to <a href="/demand/123">your admission demand</a>',)
```

Note : you can inlude HTML in your message content, it will be rendered as  is in the front-end notification component. It is advised to use only  simple formatting HTML tags (a, strong, em, br).

## Creating an email notification

An email notification is a email message that will be sent to the user once processed :

```
from osis_notification import create_email_notification
create_email_notification(person, message)
```

Note : it is advised to use `osis_mail_template.generate_email()` to format an EmailMessage properly