
import factory.fuzzy

class UserAccountRenewalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.UserAccountRenewalRequest'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    requested_at = factory.Faker('date')

    app_name = factory.Faker('word')

