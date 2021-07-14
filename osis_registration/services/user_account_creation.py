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
import json
import random

import requests as requests

from osis_registration import settings

SUCCESS = "success"
ERROR = "error"

def create_ldap_user_account(user_creation_request):
    # mock endpoint in debug
    if settings.DEBUG:
        random_success_status = random.choice([True, False])
        if random_success_status:
            response = {"status": SUCCESS, "message": "User created entry in db"}
        else:
            response = {"status": ERROR, "message": "Missing data"}
    else:
        response = requests.post(
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "id": str(user_creation_request.uuid),
                "datenaissance": user_creation_request.birth_date.strftime('%Y%m%d%fZ'),
                "prenom": user_creation_request.first_name,
                "nom": user_creation_request.last_name,
                "email": user_creation_request.email
            }),
            url=settings.LDAP_ACCOUNT_CREATION_URL
        )

    return response
