##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2022 Université catholique de Louvain (http://www.uclouvain.be)
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


import logging as default_logging

from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from base.models.enum import UserAccountRequestStatus
from base.models.user_account_request import UserAccountRequest
from base.services import logging
from base.services.token_generator import mail_validation_token_generator
from base.services.user_account_activation import activate_ldap_user_account
from base.views.registration import UserAccountCreationRequest
from base.views.user_account_creation_status import UserAccountCreationStatusView


class ValidateEmailView(View):
    name = 'validate_email'

    def get(self, request, uacr_uuid, token):
        try:
            account_creation_request = UserAccountRequest.objects.get(uuid=uacr_uuid)
        except UserAccountCreationRequest.DoesNotExist:
            account_creation_request = None

        if account_creation_request \
                and not account_creation_request.email_validated \
                and mail_validation_token_generator.check_token(account_creation_request, token) \
                and account_creation_request.status == UserAccountRequestStatus.PENDING.value:
            response = activate_ldap_user_account(account_creation_request)
            if 'status' in response and response['status'] == 'success':
                account_creation_request.email_validated = True
                account_creation_request.status = UserAccountRequestStatus.SUCCESS.value
                self._log_account_activation_success(account_creation_request)
            else:
                account_creation_request.status = UserAccountRequestStatus.ERROR.value
                self._log_account_activation_error(account_creation_request)
            account_creation_request.save()

        return redirect(reverse(UserAccountCreationStatusView.name, kwargs={'uacr_uuid': uacr_uuid}))

    def _log_account_activation_success(self, account_creation_request):
        logging.log_event(
            self.request,
            event_type=logging.EventType.VIEW,
            domain='osis-registration',
            description=f"email validated and user account activated for <{account_creation_request.email}>"
        )

    def _log_account_activation_error(self, account_creation_request):
        logging.log_event(
            self.request,
            event_type=logging.EventType.ERROR,
            domain='osis-registration',
            level=default_logging.ERROR,
            description=f"error occured during user account activation for <{account_creation_request.email}>"
        )
