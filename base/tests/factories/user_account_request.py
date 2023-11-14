import uuid as uuid

import factory.fuzzy

from base.models.enum import UserAccountRequestType, UserAccountRequestStatus


class UserAccountRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'base.UserAccountRequest'

    uuid = uuid.uuid4()
    email = factory.Faker('email')
    email_validated = False

    type = UserAccountRequestType.CREATION.value
    status = UserAccountRequestStatus.PENDING.value
