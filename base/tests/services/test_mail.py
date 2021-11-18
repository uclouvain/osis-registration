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

from django.test import TestCase, RequestFactory

from base.services.mail import send_validation_mail
from base.tests.factories.user_account_creation_request import UserAccountCreationRequestFactory


class MailTestCase(TestCase):

    @mock.patch('base.messaging.send_message.send_messages')
    def test_should_send_validation_mail(self, mock_send_msg):
        request = RequestFactory().get('/')
        uacr = UserAccountCreationRequestFactory()
        send_validation_mail(request, uacr)
        self.assertTrue(mock_send_msg.called)

        _, kwargs = mock_send_msg.call_args
        self.assertTrue(uacr.email in str(kwargs['message_content']['receivers']))
