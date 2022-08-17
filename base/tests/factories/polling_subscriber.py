import datetime

import factory.fuzzy

from base.tests.factories.user import UserFactory

now = datetime.datetime.now()


class PollingSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.PollingSubscriber'

    app_name = factory.SubFactory(UserFactory)
    last_poll_requested = now
