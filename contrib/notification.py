from base.models.person import Person


class EmailNotification(object):

    def __init__(
            self,
            recipient: Person,
            subject: str,
            plain_text_content: str,
            html_content: str,
    ):
        """This class must be implemented in order to use the email notification
        handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance.
        :param subject: The subject of the email notification.
        :param plain_text_content: Represent the plain text content of the notification.
        :param html_content: Represent the html content of the notification."""

        self.recipient = recipient
        self.subject = subject
        self.plain_text_content = plain_text_content
        self.html_content = html_content


class WebNotification(object):

    def __init__(self, recipient: Person, content: str):
        """This class must be implemented in order to use the web notification handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance.
        :param content: Represent the content of the notification."""

        self.recipient = recipient
        self.content = content
