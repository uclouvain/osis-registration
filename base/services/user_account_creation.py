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
from datetime import date, timedelta
from typing import Union

import requests as requests
from requests import Response
from requests.exceptions import Timeout

from base import settings
from base.services.mock_service import mock_ldap_service
from base.services.service_exceptions import CreateUserAccountErrorException

SUCCESS = "success"
ERROR = "error"


def create_ldap_user_account(user_creation_request) -> Union[Response, dict]:
    if settings.MOCK_LDAP_CALLS:
        response = mock_ldap_service()
    else:
        try:
            response = requests.post(
                headers={'Content-Type': 'application/json'},
                json={
                    "id": str(user_creation_request.request.uuid),
                    "datenaissance": user_creation_request.birth_date.strftime('%Y%m%d%fZ'),
                    "prenom": user_creation_request.first_name,
                    "nom": user_creation_request.last_name,
                    "email": user_creation_request.request.email,
                    "password": user_creation_request.password,
                    "validite": (date.today() - timedelta(days=1)).strftime('%Y%m%d')
                },
                url=settings.LDAP_ACCOUNT_CREATION_URL,
                timeout=60,
            )
        except Timeout:
            response = {"status": ERROR, "message": "Request timed out"}

        if 'status' in response and response['status'] == ERROR:
            raise CreateUserAccountErrorException(detailed_msg=response['message'])

    return response
