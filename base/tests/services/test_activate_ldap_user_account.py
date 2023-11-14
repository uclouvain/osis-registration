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
from unittest.mock import patch

from django.test import TestCase

from base import settings
from base.services.user_account_activation import activate_ldap_user_account
from base.tests.factories.user_account_request import UserAccountRequestFactory


class ActivateUserAccountServiceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.pending_request = UserAccountRequestFactory()

    @patch('base.settings.MOCK_LDAP_CALLS', False)
    @patch('base.settings.LDAP_ACCOUNT_MODIFICATION_URL', 'fake_ldap_url')
    @mock.patch('base.services.user_account_creation.requests.post')
    def test_service_should_call_endpoint_to_attempt_user_account_activation(self, mock_post):
        activate_ldap_user_account(self.pending_request)
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['url'], settings.LDAP_ACCOUNT_MODIFICATION_URL)
