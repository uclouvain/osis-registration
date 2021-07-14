
import factory.fuzzy

class UserAccountCreationRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.UserAccountCreationRequest'

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    attempt = 0
    success = False
    app_name = factory.Faker('word')

