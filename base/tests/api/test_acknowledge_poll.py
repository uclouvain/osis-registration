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

from base.api.serializers.polling_subscriber import PollingSubscriberSerializer
from base.api.views.acknowledge_poll import AcknowledgePoll
from base.tests.factories.polling_subscriber import PollingSubscriberFactory
from base.tests.factories.user import UserFactory

from dateutil import parser

class AcknowledgePollTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.subscriber = PollingSubscriberFactory(
            app_name=cls.user,
        )

    def setUp(self) -> None:
        self.token_auth_patcher = mock.patch(
            'rest_framework.authentication.TokenAuthentication.authenticate',
            return_value=(self.user, 'tokenkey')
        )
        self.mocked_get_training = self.token_auth_patcher.start()
        self.addCleanup(self.token_auth_patcher.stop)

    def test_should_update_subscriber_last_poll_requested(self):
        url = reverse(AcknowledgePoll.name)
        response = self.client.put(
            url,
            data={'last_poll_requested': datetime.datetime.now()},
            content_type='application/json'
        )
        self.subscriber.refresh_from_db()
        self.assertEqual(
            parser.parse(response.json()['last_poll_requested']),
            parser.parse(PollingSubscriberSerializer(self.subscriber).data['last_poll_requested'])
        )
