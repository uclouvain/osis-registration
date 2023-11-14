##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2022 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from unittest import mock

from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models.enum import UserAccountRequestType
from base.models.user_account_request import UserAccountRequest
from base.tests.factories.polling_subscriber import PollingSubscriberFactory
from base.tests.factories.user import UserFactory


class CreateAccountTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.subscriber = PollingSubscriberFactory(app_name=cls.user)

        cls.url = reverse('create-account')
        cls.post_data = {
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'birth_date': '2000-01-01',
            'email': 'email@email.com',
            'password': 'password'
        }

    def test_should_unauthorize_no_subscriber(self):
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_get(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        response = self.client.get(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_should_deny_creation_missing_data(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        self.post_data.pop('password')
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing data", str(response.content))
        self.assertIn("password", str(response.content))

    def test_should_deny_creation_wrong_birth_date_format(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        self.post_data['birth_date'] = "01-01-2000"
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not match format", str(response.content))

    def test_should_deny_creation_wrong_email_format(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        self.post_data['email'] = "email"
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", str(response.content))


    @mock.patch('base.api.views.create_account.create_ldap_user_account')
    def test_should_create_user_account_request_and_call_creation_service(self, mock_create):
        self.client.force_authenticate(user=self.subscriber.app_name)
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_account_request = UserAccountRequest.objects.first()
        self.assertEqual(user_account_request.email, self.post_data['email'])
        self.assertEqual(user_account_request.type, UserAccountRequestType.CREATION.name)

        self.assertTrue(mock_create.called)
