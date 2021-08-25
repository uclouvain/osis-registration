
import factory.fuzzy

class UserAccountDeletionRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.UserAccountDeletionRequest'

    email = factory.Faker('email')
    app_name = factory.Faker('word')

