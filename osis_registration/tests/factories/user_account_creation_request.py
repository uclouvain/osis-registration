
import factory.fuzzy

class UserAccountCreationRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.UserAccountCreationRequest'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    requested_at = factory.Faker('date')

    retry = 0
    account_created = False
    app_name = factory.Faker('word')

