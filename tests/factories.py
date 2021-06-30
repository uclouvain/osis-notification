import factory.fuzzy

from base.tests.factories.person import PersonFactory


class EmailNotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = "osis_notification.EmailNotification"

    person = factory.SubFactory(PersonFactory)
    built_from_module = "osis_notification.contrib.notification"
    built_from_class_name = "EmailNotification"


class WebNotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = "osis_notification.WebNotification"

    person = factory.SubFactory(PersonFactory)
    payload = factory.fuzzy.FuzzyText()
    built_from_module = "osis_notification.contrib.notification"
    built_from_class_name = "WebNotification"
