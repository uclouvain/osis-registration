import datetime

import factory.fuzzy

from base.tests.factories.polling_subscriber import PollingSubscriberFactory

now = datetime.datetime.now()

class UserAccountRequestResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.UserAccountRequestResult'

    email = factory.Faker('email')
    request_type = 'CREATION'
    status = 'SUCCESS'
    app = factory.SubFactory(PollingSubscriberFactory)
    updated_at = now
