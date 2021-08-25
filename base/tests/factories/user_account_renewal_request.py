
import factory.fuzzy

class UserAccountRenewalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.UserAccountRenewalRequest'

    email = factory.Faker('email')
    app_name = factory.Faker('word')

