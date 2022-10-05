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

from django.views.generic import TemplateView

from base import settings
from base.models.user_account_request import UserAccountRequest
from base.services import logging


@logging.log_event_decorator(
    logging.EventType.VIEW,
    "osis-registration",
    "access user account status view"
)
class UserAccountCreationStatusView(TemplateView):
    name = 'user_account_status'
    template_name = 'registration_status/user_account_status.html'

    def get_context_data(self, **kwargs):
        account_request = UserAccountRequest.objects.get(uuid=kwargs['uacr_uuid'])
        redirection_url = account_request.subscriber.redirection_url \
            if account_request.subscriber else settings.OSIS_PORTAL_URL
        return {
            'account_request': account_request,
            'login_redirection_url': redirection_url
        }
