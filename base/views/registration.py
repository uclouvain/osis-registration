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
import logging as default_logging
import re
from dataclasses import dataclass

import requests
from captcha import views
from django.contrib import messages
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from ratelimit.decorators import ratelimit
from requests.exceptions import MissingSchema

from base import settings
from base.forms.registration import RegistrationForm
from base.models.enum import UserAccountRequestType
from base.models.polling_subscriber import PollingSubscriber
from base.models.user_account_request import UserAccountRequest
from base.override_django_captcha import captcha_audio
from base.services import mail, logging
from base.services.service_exceptions import CreateUserAccountErrorException
from base.services.user_account_creation import create_ldap_user_account
from base.utils import PasswordCheckErrorEnum, PasswordCheckServiceBadRequestException
from base.views.user_account_creation_status import UserAccountCreationStatusView


@dataclass
class UserAccountCreationRequest:
    request: 'UserAccountRequest'
    first_name: str
    last_name: str
    birth_date: 'datetime'
    password: str


@method_decorator(ratelimit(key='ip', rate=settings.REQUESTS_RATE_LIMIT, block=True, method='POST'), name='post')
@logging.log_event_decorator(
    logging.EventType.VIEW,
    "osis-registration",
    "access registration form"
)
class RegistrationFormView(FormView):
    name = 'registration'
    template_name = 'home.html'
    form_class = RegistrationForm

    user_account_request = None
    subscriber = None

    def dispatch(self, request, *args, **kwargs):
        self.subscriber = self._get_subscriber()
        return super(RegistrationFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        birth_date = "{}-{}-{}".format(
            self.request.POST['birth_date_year'],
            self.request.POST['birth_date_month'],
            self.request.POST['birth_date_day']
        )

        try:
            if not self.password_valid(form):
                return super().form_invalid(form)
        except (PasswordCheckServiceBadRequestException, MissingSchema) as e:
            self._log_password_check_attempt_failed(self.request.POST['email'], e.msg)

        self.user_account_request = UserAccountRequest(
            email=self.request.POST['email'],
            type=UserAccountRequestType.CREATION.value,
            subscriber=self.subscriber
        )

        user_account_creation_request = UserAccountCreationRequest(
            request=self.user_account_request,
            first_name=self.request.POST['first_name'],
            last_name=self.request.POST['last_name'],
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d'),
            password=self.request.POST['password'],
        )

        self._log_user_creation_attempt(user_account_creation_request)

        try:
            redirection_url = self.subscriber.redirection_url if self.subscriber else settings.OSIS_PORTAL_URL
            user_account_creation_response = create_ldap_user_account(user_account_creation_request, redirection_url)
        except CreateUserAccountErrorException as e:
            self._log_user_creation_error(user_account_creation_request)
            messages.add_message(self.request, message=mark_safe(e.msg), level=messages.ERROR)
            form.add_error('email', mark_safe(
                # error msg is capitalized after each punctuation
                re.sub("(^[a-zA-Z])|(^|[.?!])(\s)+([a-zA-Z])", lambda p: p.group(0).upper(), e.error_msg)
            ))
            return super().form_invalid(form)

        if 'status' in user_account_creation_response and user_account_creation_response['status'] == 'success':
            self.user_account_request.save()
            mail.send_validation_mail(self.request, user_account_creation_request)
        else:
            messages.add_message(
                self.request,
                message=_("An error occured while sending the creation request. Please try again later."),
                level=messages.ERROR
            )
            return super().form_invalid(form)

        return super().form_valid(form)

    def _get_subscriber(self):
        try:
            subscriber = PollingSubscriber.objects.get(app_name__username=self.request.GET.get('source'))
        except PollingSubscriber.DoesNotExist:
            subscriber = None
        return subscriber

    def _log_user_creation_error(self, user_account_creation_request):
        logging.log_event(
            self.request,
            event_type=logging.EventType.ERROR,
            domain='osis-registration',
            level=default_logging.ERROR,
            description=f"a user account with the given email"
                        f" <{user_account_creation_request.request.email}> already exists"
        )

    def _log_user_creation_attempt(self, user_account_creation_request):
        logging.log_event(
            request=self.request,
            event_type=logging.EventType.CREATE,
            domain="osis-registration",
            description=f"create LDAP user account for "
                        f"{user_account_creation_request.first_name}, {user_account_creation_request.last_name} "
                        f"<{user_account_creation_request.request.email}>"
        )

    def _log_password_check_attempt_failed(self, email, exception_msg):
        logging.log_event(
            request=self.request,
            event_type=logging.EventType.ERROR,
            domain="osis-registration",
            description=f"password check failed for <{email}>: {exception_msg}"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'data_protection_policy_url': settings.DATA_PROTECTION_POLICY_URL,
            'log_in_url': self.subscriber.redirection_url if self.subscriber else settings.OSIS_PORTAL_URL,
            'form_visible': bool(self.request.GET.get('form_visible', False)),
        })
        return context

    def get_success_url(self):
        return reverse(UserAccountCreationStatusView.name, kwargs={'uacr_uuid': self.user_account_request.uuid})

    def password_valid(self, form):
        if not settings.MOCK_LDAP_CALLS:
            password_valid_check = requests.post(url=settings.PASSWORD_CHECK_URL, data={
                "pwd": self.request.POST['password'],
                "first_name": self.request.POST['first_name'],
                "last_name": self.request.POST['last_name'],
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


# replace captcha audio with custom captcha audio generator using espeak
views.captcha_audio = captcha_audio
