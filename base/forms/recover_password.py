##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2024 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

import requests
from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    NumericPasswordValidator, CommonPasswordValidator
from django.utils.translation import gettext_lazy as _

from base.admin import User

ACCOUNT_TYPE_INTERNAL = 'internal'
ACCOUNT_TYPE_EXTERNAL = 'external'

class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(label=_('Private email address'), max_length=100, required=True)

    def check_account_type(self):
        email = self.cleaned_data['email']
        try:
            response = requests.get(
                f"{settings.LDAP_ACCOUNT_IS_SWITCHED_EMAIL_URL}{email}",
                timeout=60
            )
            if response.status_code == 200 and response.json()['status'] == 'success':
                return ACCOUNT_TYPE_INTERNAL
        except requests.RequestException:
            return ACCOUNT_TYPE_EXTERNAL
        return ACCOUNT_TYPE_EXTERNAL


class ModifyPasswordForm(forms.Form):

    user_account = None

    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        required=True,
        widget=forms.PasswordInput(render_value=True),
        validators=[
            MinimumLengthValidator(min_length=12).validate,
            NumericPasswordValidator().validate,
            CommonPasswordValidator().validate
        ],
    )

    def __init__(self, *args, **kwargs):
        self.user_account = kwargs.pop('user_account')
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']

        user_info = User(
            first_name=self.user_account['prenom'],
            last_name=self.user_account['nom'],
            email=self.user_account['email'],
        )

        UserAttributeSimilarityValidator().validate(password=password, user=user_info)

        return password
