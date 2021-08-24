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
import json

import uuid
from django.shortcuts import reverse
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from osis_registration import settings
from osis_registration.api.views.check_account_creation_request import UserAccountCreationCheck
from osis_registration.tests.factories.user import UserFactory
from osis_registration.tests.factories.user_account_creation_request import UserAccountCreationRequestFactory


class UserAccountCreationCheckTestCase(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_should_retrieve_account_creation_request_status_not_succeeded_when_not_processed(self):
        uacr = UserAccountCreationRequestFactory()
        url = reverse(UserAccountCreationCheck.name, kwargs={'uacr_uuid': uacr.uuid})
        json_response = self.client.get(url).json()
        self.assertFalse(json_response['success'])

    def test_should_retrieve_account_creation_request_status_ongoing_when_attempts_less_than_limit(self):
        uacr = UserAccountCreationRequestFactory(attempt=settings.REQUEST_ATTEMPT_LIMIT-1)
        url = reverse(UserAccountCreationCheck.name, kwargs={'uacr_uuid': uacr.uuid})
        json_response = self.client.get(url).json()
        self.assertTrue(json_response['ongoing'])
