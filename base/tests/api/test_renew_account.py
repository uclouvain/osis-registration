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
from datetime import datetime
from unittest import mock

from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models.enum import UserAccountRequestType
from base.models.user_account_request import UserAccountRequest
from base.tests.factories.polling_subscriber import PollingSubscriberFactory
from base.tests.factories.user import UserFactory


class RenewAccountTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.subscriber = PollingSubscriberFactory(app_name=cls.user)

        cls.url = reverse('renew-account')
        cls.renewal_data = {
            'email': 'email@email.com',
            'validity_days': 365
        }

    def test_should_unauthorize_no_subscriber(self):
        response = self.client.post(self.url, data=self.renewal_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_get(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        response = self.client.get(self.url, data=self.renewal_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_should_deny_renewal_missing_data(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        self.renewal_data.pop('email')
        response = self.client.post(self.url, data=self.renewal_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing data", str(response.content))
        self.assertIn("email", str(response.content))

    def test_should_deny_renewal_wrong_email_format(self):
        self.client.force_authenticate(user=self.subscriber.app_name)
        self.renewal_data['email'] = "email"
        response = self.client.post(self.url, data=self.renewal_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", str(response.content))

    @mock.patch('base.api.views.renew_account.renew_ldap_user_account_validity', return_value={
        'validite': datetime.now().strftime("%Y%m%d")
    })
    def test_should_create_renewal_user_account_request_and_call_renewal_service(self, mock_renew):
        self.client.force_authenticate(user=self.subscriber.app_name)
        response = self.client.post(self.url, data=self.renewal_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_account_request = UserAccountRequest.objects.first()
        self.assertEqual(user_account_request.email, self.renewal_data['email'])
        self.assertEqual(user_account_request.type, UserAccountRequestType.RENEWAL.name)

        self.assertTrue(mock_renew.called)
