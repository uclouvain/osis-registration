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
import uuid
from dataclasses import dataclass
from types import SimpleNamespace

from captcha import views
from django.shortcuts import render
from django.utils.datetime_safe import date, datetime
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

from base import settings
from base.forms.registration import RegistrationForm
from base.models.enum import UserAccountRequestType
from base.models.polling_subscriber import get_osis_registration_subscriber, PollingSubscriber
from base.models.user_account_request import UserAccountRequest
from base.override_django_captcha import captcha_audio
from base.services import mail
from base.services.token_generator import mail_validation_token_generator
from base.services.user_account_creation import create_ldap_user_account


@dataclass
class UserAccountCreationRequest:
    request: 'UserAccountRequest'
    first_name: str
    last_name: str
    birth_date: 'datetime'
    password: str
    app: 'PollingSubscriber'


class RegistrationFormView(FormView):
    name = 'registration'
    template_name = 'home.html'
    success_url = '/user_account_creation_requested'
    form_class = RegistrationForm

    def form_valid(self, form):
        birth_date = "{}-{}-{}".format(
            self.request.POST['birth_date_year'],
            self.request.POST['birth_date_month'],
            self.request.POST['birth_date_day']
        )

        request = UserAccountRequest(
            email=self.request.POST['email'],
            type=UserAccountRequestType.CREATION
        )

        user_account_creation_request = UserAccountCreationRequest(
            request=request,
            first_name=self.request.POST['first_name'],
            last_name=self.request.POST['last_name'],
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d'),
            password=self.request.POST['password'],
            app=get_osis_registration_subscriber(),
        )

        user_account_creation_response = create_ldap_user_account(user_account_creation_request)

        mail.send_validation_mail(self.request, user_account_creation_request)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'data_protection_policy_url': settings.DATA_PROTECTION_POLICY_URL})
        return context

# replace captcha audio with custom captcha audio generator using espeak
views.captcha_audio = captcha_audio


class UserAccountCreationRequestedView(TemplateView):
    name = 'user_account_creation_requested'
    template_name = 'registration_status/user_account_creation_requested.html'
    

class ValidateEmailView(View):
    name = 'validate_email'

    def get(self, request, uacr_uuid, token):
        try:
            account_creation_request = UserAccountCreationRequest.objects.get(uuid=uacr_uuid)
        except UserAccountCreationRequest.DoesNotExist:
            account_creation_request = None

        if account_creation_request and mail_validation_token_generator.check_token(account_creation_request, token):
            account_creation_request.email_validated = True
            account_creation_request.save()

        return render(request, 'registration_status/email_validated.html', context={
            'uacr_uuid': uacr_uuid,
            'uacr_email': account_creation_request.email,
            'account_configuration_url': settings.LDAP_ACCOUNT_CONFIGURATION_URL
        })

