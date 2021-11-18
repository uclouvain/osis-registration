##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2021 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.test import TestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from base.api.views.create_account import CreateAccount
from base.models.user_account_creation_request import UserAccountCreationRequest
from base.tests.factories.polling_subscriber import PollingSubscriberFactory


class PollRequestResultsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subscriber = PollingSubscriberFactory(app_name__username='polling_application')
        cls.request_data = {
            'first_name': 'test',
            'last_name': 'test',
            'birth_date': '2000-01-01',
            'email': 'test@test.xyz'
        }

    @mock.patch('rest_framework.authentication.TokenAuthentication.authenticate')
    def test_should_create_user_account_creation_request_with_token_related_app_name(self, mock_token_auth):
        mock_token_auth.return_value = (self.subscriber.app_name, 'tokenkey')
        url = reverse(CreateAccount.name)
        response = self.client.post(url, data=self.request_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # request created with token related app_name (user)
        uacr = UserAccountCreationRequest.objects.get(uuid=response.json()['uuid'])
        self.assertEqual(uacr.app, self.subscriber)

    def test_should_not_authorize_user_creation_when_no_token_provided(self):
        url = reverse(CreateAccount.name)
        response = self.client.post(url, data=self.request_data)

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
