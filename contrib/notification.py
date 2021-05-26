from base.models.person import Person


class EmailNotification(object):

    def __init__(self, recipient: Person, content: str):
        """This class must be implemented in order to use the email notification
        handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance.
        :param content: Represent the content of the notification."""
        self.recipient = recipient
        self.content = content


class WebNotification(object):

    def __init__(self, recipient: Person, content: str):
        """This class must be implemented in order to use the web notification handlers.

        :param recipient: Represent the notification's recipient and must be a Person
        instance.
        :param content: Represent the content of the notification."""
        self.recipient = recipient
        self.content = content
