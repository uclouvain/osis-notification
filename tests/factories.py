import factory.fuzzy

from base.tests.factories.person import PersonFactory


class EmailNotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = "osis_notification.EmailNotification"

    person = factory.SubFactory(PersonFactory)


class WebNotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = "osis_notification.WebNotification"

    person = factory.SubFactory(PersonFactory)
    payload = factory.fuzzy.FuzzyText()
