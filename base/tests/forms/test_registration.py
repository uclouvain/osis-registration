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

from django.test.testcases import SimpleTestCase

from base.forms.registration import RegistrationForm


class RegistrationFormTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.user_info = {
            'first_name': 'UserFirstName',
            'last_name': 'UserLastName',
            'email': 'test@osis.org',
            'birth_date': date.today(),
            'password': 'acceptable_secret',
        }
        self._patch_captcha()

    def _patch_captcha(self):
        captcha_patcher = mock.patch('captcha.fields.CaptchaField.clean', return_value='CAPTCHA')
        captcha_patcher.start()
        self.addCleanup(captcha_patcher.stop)

    def test_form_is_valid(self):
        form = RegistrationForm(data=self.user_info)
        self.assertTrue(form.is_valid())

    def test_password_should_be_long_enough(self):
        self.user_info['password'] = 'short'
        form = RegistrationForm(data=self.user_info)
        self.assertFalse(form.is_valid())

    def test_password_should_be_not_only_numeric(self):
        self.user_info['password'] = '123456789'
        form = RegistrationForm(data=self.user_info)
        self.assertFalse(form.is_valid())

    def test_password_should_be_dissimilar_from_user_info(self):
        self.user_info['password'] = 'FirstName'
        form = RegistrationForm(data=self.user_info)
        self.assertFalse(form.is_valid())
