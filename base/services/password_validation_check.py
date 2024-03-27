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
import re

import requests
from django.conf import settings

from base.utils import PasswordCheckErrorEnum, PasswordCheckServiceBadRequestException


def password_valid(form, first_name, last_name, password):
    if not settings.MOCK_LDAP_CALLS:
        password_valid_check = requests.post(url=settings.PASSWORD_CHECK_URL, data={
            "pwd": password,
            "first_name": first_name,
            "last_name": last_name,
        }).json()

        if not password_valid_check['result']:
            missing_param_error_code, _ = PasswordCheckErrorEnum.MISSING_PARAMETERS.value
            if password_valid_check['error code'] == missing_param_error_code:
                raise PasswordCheckServiceBadRequestException

            error_msg = PasswordCheckErrorEnum.get_error_msg(password_valid_check['error code'])

            unsupported_char, _ = PasswordCheckErrorEnum.UNSUPPORTED_CHAR.value
            if password_valid_check['error code'] == unsupported_char:
                regexp = '[^a-zA-Z0-9À-ÿ#()!?_+*/=$%,.;:@&<>§-]'
                error_chars = re.findall(regexp, password)
                error_msg += f": {' '.join(error_chars)}"

            form.add_error('password', error_msg)
            return False

    return True
