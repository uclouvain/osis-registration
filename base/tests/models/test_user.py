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

from django.test.testcases import TestCase

from base.models.user import OsisRegistrationUserCreationForm


class OsisRegistrationUserCreationAdminForm(TestCase):

    def test_should_require_user_creation_form_in_admin_with_username_only(self):
        form = OsisRegistrationUserCreationForm()
        self.assertTrue(form.base_fields['username'].required)
        self.assertFalse(form.base_fields['password1'].required)
        self.assertFalse(form.base_fields['password2'].required)

    @mock.patch('secrets.token_hex', return_value='generated_password')
    def test_should_generate_password_on_form_submit(self, mock_token_hex):
        form = OsisRegistrationUserCreationForm(data={'username': 'test'})
        form.is_valid()
        self.assertEqual(form.cleaned_data['password1'], 'generated_password')
        self.assertEqual(form.cleaned_data['password2'], 'generated_password')
