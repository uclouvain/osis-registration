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

from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from ratelimit.decorators import ratelimit

from base import settings
from base.forms.check_status import CheckStatusForm
from base.services import logging, mail
from base.services.service_exceptions import RetrieveUserAccountInformationErrorException
from base.services.user_account_creation import _get_existing_account_request
from base.services.user_account_information import get_ldap_user_account_information
from base.views.user_account_creation_status import UserAccountCreationStatusView


@method_decorator(ratelimit(key='ip', rate=settings.RESET_SEND_MAIL_RATE_LIMIT, block=True, method='POST'), name='post')
@logging.log_event_decorator(
    logging.EventType.VIEW,
    "osis-registration",
    "access check status form"
)
class CheckStatusFormView(FormView):
    name = 'check-status'
    template_name = 'check_status.html'
    form_class = CheckStatusForm

    user_account = None
    existing_account_request = None

    def form_valid(self, form):
        try:
            self.user_account = get_ldap_user_account_information(form.cleaned_data['email'])
            self.existing_account_request = _get_existing_account_request(self.user_account['email'])
            if not self.existing_account_request.email_validated:
                mail.send_validation_mail(self.request, self.existing_account_request)
        except RetrieveUserAccountInformationErrorException:
            form.add_error(
                'email',
                mark_safe(
                    _("No account creation request been found with the given email. You may have to create an account first: <br/><a href='{}'>Create account</a>").format(
                        reverse('registration') + "?source=admission")
                    )
            )
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'admission_registration_url': reverse('registration') + f"?source=admission"
        })
        return context

    def get_success_url(self):
        if not self.existing_account_request.email_validated:
            self._log_validate_mail_link_sent(self.user_account['email'])
            messages.add_message(
                self.request,
                message=_("A mail with instructions to validate your email has been sent to {}").format(
                    self.user_account['email']
                ),
                level=messages.SUCCESS
            )
        return reverse(UserAccountCreationStatusView.name, kwargs={'uacr_uuid': self.existing_account_request.uuid})

    def _log_validate_mail_link_sent(self, email):
        logging.log_event(
            request=self.request,
            event_type=logging.EventType.VIEW,
            domain="osis-registration",
            description=f"validate mail link sent to <{email}>"
        )
