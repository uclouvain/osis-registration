
import factory.fuzzy

from osis_registration.tests.factories.user import UserFactory


class PollingSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.PollingSubscriber'

    app_name = factory.SubFactory(UserFactory)
