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
from datetime import date
from unittest import mock

from django.contrib import messages
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from base.models.user_account_request import UserAccountRequest
from base.tests.factories.polling_subscriber import PollingSubscriberFactory
from base.tests.factories.user import UserFactory


class RegistrationFormViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        PollingSubscriberFactory(app_name=UserFactory(username='osis_registration'))
        birth_date = date.today()
        cls.user_info = {
            'first_name': 'UserFirstName',
            'last_name': 'UserLastName',
            'email': 'test@osis.org',
            'birth_date_year': birth_date.year,
            'birth_date_month': birth_date.month,
            'birth_date_day': birth_date.day,
            'password': 'acceptable_secret',
        }
        cls.url = reverse('registration')

    def setUp(self) -> None:
        self._patch_captcha()

    def _patch_captcha(self):
        captcha_patcher = mock.patch('captcha.fields.CaptchaField.clean', return_value='CAPTCHA')
        captcha_patcher.start()
        self.addCleanup(captcha_patcher.stop)

    def test_access_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    @mock.patch('base.views.registration.create_ldap_user_account', return_value={'status': 'success'})
    @mock.patch('base.views.registration.RegistrationFormView.password_valid', return_value=True)
    def test_post_form_valid_should_create_request_and_redirect_to_user_account_status_view(
            self, mock_create, mock_chk_pwd
    ):
        response = self.client.post(self.url, data=self.user_info)
        user_account_request = UserAccountRequest.objects.first()
        success_url = reverse('user_account_status', kwargs={'uacr_uuid': str(user_account_request.uuid)})
        self.assertRedirects(response, success_url)

    @mock.patch('base.views.registration.create_ldap_user_account', return_value={'status': 'error'})
    @mock.patch('base.views.registration.RegistrationFormView.password_valid', return_value=True)
    def test_service_should_reload_view_with_error_msg(self, mock_create, mock_chk_pwd):
        response = self.client.post(self.url, data=self.user_info)
        msg_level = next(m.level for m in get_messages(response.wsgi_request))
        self.assertEqual(msg_level, messages.ERROR)
        self.assertTemplateUsed('home.html')
