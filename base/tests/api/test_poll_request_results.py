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
import datetime
from unittest import mock

from django.shortcuts import reverse
from django.test import TestCase

from base.api.serializers.user_account_request_result import UserAccountRequestResultSerializer
from base.api.views.poll_request_results import PollRequestResults
from base.models import UserAccountRequestResult
from base.tests.factories.polling_subscriber import PollingSubscriberFactory
from base.tests.factories.user import UserFactory
from base.tests.factories.user_account_request_result import UserAccountRequestResultFactory


class PollRequestResultsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        subscriber = PollingSubscriberFactory(
            app_name=cls.user,
        )

        old_request_result = UserAccountRequestResultFactory(app=subscriber)
        _fake_update_time_in_past(old_request_result)

        cls.new_request_result = UserAccountRequestResultFactory(app=subscriber)

    def setUp(self) -> None:
        self.token_auth_patcher = mock.patch(
            'rest_framework.authentication.TokenAuthentication.authenticate',
            return_value=(self.user, 'tokenkey')
        )
        self.mocked_get_training = self.token_auth_patcher.start()
        self.addCleanup(self.token_auth_patcher.stop)

    def test_should_retrieve_new_results_since_last_poll(self):
        url = reverse(PollRequestResults.name)
        response = self.client.get(url)
        self.assertEqual(response.json(), [UserAccountRequestResultSerializer(self.new_request_result).data])

def _fake_update_time_in_past(request_result):
    UserAccountRequestResult.objects.filter(pk=request_result.pk).update(
        updated_at=datetime.datetime.now() - datetime.timedelta(minutes=5)
    )
