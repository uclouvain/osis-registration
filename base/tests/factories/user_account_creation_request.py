import datetime

import factory.fuzzy

from base.tests.factories.polling_subscriber import PollingSubscriberFactory

now = datetime.datetime.now()

class UserAccountCreationRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.UserAccountCreationRequest'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    email_validated = False

    birth_date = factory.fuzzy.FuzzyDate(
        datetime.datetime(now.year-80, 1, 1),
        datetime.datetime(now.year-18, 1, 1)
    )

    attempt = 0
    success = False
    app = factory.SubFactory(PollingSubscriberFactory)

