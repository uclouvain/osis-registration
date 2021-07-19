
import factory.fuzzy

class UserAccountDeletionRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'osis_registration.UserAccountDeletionRequest'

    email = factory.Faker('email')
    app_name = factory.Faker('word')

