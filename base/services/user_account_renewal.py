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
from datetime import date, timedelta
from typing import Union

import requests as requests
from requests import Response
from requests.exceptions import Timeout

from base import settings
from base.services import logging
from base.services.mock_service import mock_ldap_service
from base.services.service_exceptions import RenewUserAccountValidityErrorException

ERROR = "error"

@logging.log_event_decorator(
    logging.EventType.UPDATE,
    "osis-registration",
    "extends LDAP user account validity for {email} by {validity_days} days from today"
)
def renew_ldap_user_account_validity(request, account_id, email, validity_days) -> Union[Response, dict]:
    if settings.MOCK_LDAP_CALLS:
        response = mock_ldap_service()
    else:
        try:
            response = requests.post(
                headers={'Content-Type': 'application/json'},
                json={
                    "id": account_id,
                    "validite": (date.today() + timedelta(days=int(validity_days))).strftime('%Y%m%d')
                },
                url=settings.LDAP_ACCOUNT_MODIFICATION_URL,
                timeout=60,
            ).json()
        except Timeout:
            response = {"status": ERROR, "message": "Request timed out"}

    if 'status' in response and response['status'] == ERROR:
        raise RenewUserAccountValidityErrorException(detailed_msg=response['message'])

    return response
