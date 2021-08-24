import datetime

import factory.fuzzy

from osis_registration.tests.factories.user import UserFactory

now = datetime.datetime.now()

class PollingSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.PollingSubscriber'

    app_name = factory.SubFactory(UserFactory)
    last_poll_requested = now
