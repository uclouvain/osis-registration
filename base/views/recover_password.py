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
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from ratelimit.decorators import ratelimit
from requests.exceptions import MissingSchema

from base import settings
from base.forms.recover_password import RecoverPasswordForm, ModifyPasswordForm
from base.services import logging
from base.services.mail import send_reset_password_mail
from base.services.service_exceptions import RetrieveUserAccountInformationErrorException
from base.services.token_generator import password_reset_token_generator
from base.services.user_account_information import get_ldap_user_account_information
from base.utils import PasswordCheckErrorEnum, PasswordCheckServiceBadRequestException


@method_decorator(ratelimit(key='ip', rate=settings.REQUESTS_RATE_LIMIT, block=True, method='POST'), name='post')
@logging.log_event_decorator(
    logging.EventType.VIEW,
    "osis-registration",
    "access recover password form"
)
class RecoverPasswordFormView(FormView):
    name = 'recover_password'
    template_name = 'recover_password.html'
    form_class = RecoverPasswordForm

    user_account = None

    def form_valid(self, form):
        try:
            self.user_account = get_ldap_user_account_information(form.cleaned_data['email'])
            send_reset_password_mail(self.request, self.user_account['email'])
        except RetrieveUserAccountInformationErrorException:
            form.add_error('email', "Email not found")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'recover_password': True,
            'admission_registration_url': reverse('registration') + f"?source=admission"
        })
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            message=_("A mail with instructions to reset password has been sent to {}").format(
                self.user_account['email']
            ),
            level=messages.SUCCESS
        )
        return reverse(self.name) + f"?reset_mail={self.user_account['email']}"



@method_decorator(ratelimit(key='ip', rate=settings.REQUESTS_RATE_LIMIT, block=True, method='POST'), name='post')
@logging.log_event_decorator(
    logging.EventType.VIEW,
    "osis-registration",
    "access modify password form"
)
class ModifyPasswordFormView(FormView):
    name = 'modify_password'
    template_name = 'modify_password.html'
    form_class = ModifyPasswordForm

    user_account = None

    def get(self, request, *args, **kwargs):
        if password_reset_token_generator.check_token(kwargs['email'], kwargs['token']):
            return super().get(request, *args, **kwargs)
        messages.add_message(
            self.request,
            message=_("The link provided for password reset is invalid or expired. Please try again."),
            level=messages.ERROR
        )
        return redirect(reverse('registration') + "?source=admission")

    def post(self, request, *args, **kwargs):
        if password_reset_token_generator.check_token(kwargs['email'], kwargs['token']):
            self.user_account = get_ldap_user_account_information(kwargs['email'])
            return super().post(request, *args, **kwargs)
        messages.add_message(
            self.request,
            message=_("The link provided for password reset is invalid or expired. Please try again."),
            level=messages.ERROR
        )
        return redirect(reverse('registration') + "?source=admission")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_account'] = self.user_account
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'recover_password': True,
            'admission_registration_url': reverse('registration') + f"?source=admission"
        })
        return context

    def form_valid(self, form):
        try:
            if not self.password_valid(form, self.user_account):
                return super().form_invalid(form)
            return super().form_valid(form)
        except (PasswordCheckServiceBadRequestException, MissingSchema) as e:
            self._log_password_check_attempt_failed(self.request.POST['email'], e.msg)

    def get_success_url(self):
        messages.add_message(
            self.request,
            message=_("Password successfully reset for {}. You may now try to log in.").format(self.kwargs['email']),
            level=messages.SUCCESS
        )
        return reverse('registration') + f"?source=admission"

    def password_valid(self, form, user_info):
        if not settings.MOCK_LDAP_CALLS:
            password_valid_check = requests.post(url=settings.PASSWORD_CHECK_URL, data={
                "pwd": self.request.POST['password'],
                "first_name": user_info['first_name'],
                "last_name": user_info['last_name'],
            }).json()

            if not password_valid_check['result']:
                missing_param_error_code, _ = PasswordCheckErrorEnum.MISSING_PARAMETERS.value
                if password_valid_check['error code'] == missing_param_error_code:
                    raise PasswordCheckServiceBadRequestException

                error_msg = PasswordCheckErrorEnum.get_error_msg(password_valid_check['error code'])

                unsupported_char, _ = PasswordCheckErrorEnum.UNSUPPORTED_CHAR.value
                if password_valid_check['error code'] == unsupported_char:
                    regexp = '[^a-zA-Z0-9À-ÿ#()!?_+*/=$%,.;:@&<>§-]'
                    error_chars = re.findall(regexp, self.request.POST['password'])
                    error_msg += f": {' '.join(error_chars)}"

                form.add_error('password', error_msg)
                return False

        return True

    def _log_password_check_attempt_failed(self, email, exception_msg):
        logging.log_event(
            request=self.request,
            event_type=logging.EventType.ERROR,
            domain="osis-registration",
            description=f"password check failed for <{email}>: {exception_msg}"
        )
