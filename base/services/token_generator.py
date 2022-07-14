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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.datetime_safe import datetime


class MailValidationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user_account_creation_request, timestamp):
        """
        Hash the user account creation request's key, email, timestamp to produce a token
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually invalidates the token.
        """
        uacr = user_account_creation_request
        return f'{uacr.request.uuid}{uacr.request.email}{datetime.now()}'

mail_validation_token_generator = MailValidationTokenGenerator()