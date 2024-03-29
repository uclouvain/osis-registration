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

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.views import View

from base.models.enum import UserAccountRequestStatus
from base.models.user_account_request import UserAccountRequest
from base.services import logging
from base.services.token_generator import mail_validation_token_generator
from base.services.user_account_activation import activate_ldap_user_account
from base.views.check_status import CheckStatusFormView
from base.views.user_account_creation_status import UserAccountCreationStatusView


class ValidateEmailView(View):
    name = 'validate_email'

    def get(self, request, uacr_uuid, token):
        try:
            account_creation_request = UserAccountRequest.objects.get(uuid=uacr_uuid)
        except UserAccountRequest.DoesNotExist:
            account_creation_request = None

        token_valid = mail_validation_token_generator.check_token(account_creation_request, token)

        if account_creation_request \
                and not account_creation_request.email_validated \
                and token_valid \
                and account_creation_request.status != UserAccountRequestStatus.SUCCESS.value:
            response = activate_ldap_user_account(account_creation_request)
            if 'status' in response and response['status'] == 'success':
                account_creation_request.email_validated = True
                account_creation_request.status = UserAccountRequestStatus.SUCCESS.value
                self._log_account_activation_success(account_creation_request)
            else:
                account_creation_request.status = UserAccountRequestStatus.ERROR.value
                self._log_account_activation_error(account_creation_request)

        elif not token_valid:
            if account_creation_request.email_validated:
                messages.add_message(
                    self.request,
                    message=gettext("Your email has been validated. You may log in already."),
                    level=messages.SUCCESS
                )
            else:
                messages.add_message(
                    self.request,
                    message=mark_safe(gettext(
                        "The link provided for mail validation is invalid or expired. "
                        "Please try again. You may also <a href='{}'>check the status of your request</a>."
                    ).format(reverse(CheckStatusFormView.name))),
                    level=messages.ERROR
                )
                self._log_mail_validation_error(account_creation_request)
            return redirect(reverse('registration') + "?source=admission")

        try:
            account_creation_request.save()
        except ValidationError:
            self._log_save_request_error(account_creation_request)

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

    def _log_mail_validation_error(self, account_creation_request):
        logging.log_event(
            self.request,
            event_type=logging.EventType.ERROR,
            domain='osis-registration',
            level=default_logging.ERROR,
            description=f"error occured during mail validation for <{account_creation_request.email}>"
        )

    def _log_save_request_error(self, account_creation_request):
        logging.log_event(
            self.request,
            event_type=logging.EventType.ERROR,
            domain='osis-registration',
            level=default_logging.ERROR,
            description=f"save request error for {account_creation_request.email}"
                        f"(uuid:{account_creation_request.uuid})"
        )
