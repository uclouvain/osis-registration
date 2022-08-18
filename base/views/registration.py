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
from dataclasses import dataclass

from captcha import views
from django.contrib import messages
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from base import settings
from base.forms.registration import RegistrationForm
from base.models.enum import UserAccountRequestType
from base.models.polling_subscriber import get_osis_registration_subscriber, PollingSubscriber
from base.models.user_account_request import UserAccountRequest
from base.override_django_captcha import captcha_audio
from base.services import mail
from base.services.user_account_creation import create_ldap_user_account
from base.views.user_account_creation_status import UserAccountCreationStatusView


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
    form_class = RegistrationForm

    user_account_request = None

    def form_valid(self, form):
        birth_date = "{}-{}-{}".format(
            self.request.POST['birth_date_year'],
            self.request.POST['birth_date_month'],
            self.request.POST['birth_date_day']
        )

        self.user_account_request = UserAccountRequest(
            email=self.request.POST['email'],
            type=UserAccountRequestType.CREATION.value
        )

        user_account_creation_request = UserAccountCreationRequest(
            request=self.user_account_request,
            first_name=self.request.POST['first_name'],
            last_name=self.request.POST['last_name'],
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d'),
            password=self.request.POST['password'],
            app=get_osis_registration_subscriber(),
        )

        user_account_creation_response = create_ldap_user_account(user_account_creation_request)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'data_protection_policy_url': settings.DATA_PROTECTION_POLICY_URL})
        return context

    def get_success_url(self):
        return reverse(UserAccountCreationStatusView.name, kwargs={'uacr_uuid': self.user_account_request.uuid})


# replace captcha audio with custom captcha audio generator using espeak
views.captcha_audio = captcha_audio


