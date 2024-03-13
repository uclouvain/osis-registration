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
from django.utils.translation import gettext as _
from requests import Response
from requests.exceptions import Timeout

from base import settings
from base.services.mock_service import mock_ldap_service
from base.services.service_exceptions import CreateUserAccountErrorException

SUCCESS = "success"
ERROR = "error"


def create_ldap_user_account(user_creation_request, redirection_url=None) -> Union[Response, dict]:
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
                    "validite": (date.today() - timedelta(days=1)).strftime('%Y%m%d'),
                    "type": "A",
                },
                url=settings.LDAP_ACCOUNT_CREATION_URL,
                timeout=60,
            ).json()
        except Timeout:
            response = {"status": ERROR, "message": "Request timed out"}

        if response.get('status') == ERROR:
            if _is_ldap_constraint_email_exists_raised(response):
                used_for_recovery = _('The given email <{}> is already linked as a private email address for an existing UCLouvain account').format(
                    user_creation_request.request.email
                )
                please_try_with_uclouvain = _('Please log in using your UCLouvain email address <{}>').format(
                    response.get('email', '- @student.uclouvain.be / @uclouvain.be')
                )
                log_in_link_msg = f"<a href='{redirection_url}'>{_('Log in')}</a>" if redirection_url else ""
                raise CreateUserAccountErrorException(
                    error_msg=f"{used_for_recovery}. {please_try_with_uclouvain}. {log_in_link_msg}."
                )
            if _is_email_already_used(response):
                already_exists_msg = _('a user account with the given email <{}> already exists').format(
                    user_creation_request.request.email
                )
                log_in_link_msg = f"<a href='{redirection_url}'>{_('Log in')}</a>" if redirection_url else ""
                raise CreateUserAccountErrorException(
                    error_msg=f"{already_exists_msg}.<br/>{log_in_link_msg}"
                )
            if _is_ldap_constraint_wrong_password_raised(response):
                raise CreateUserAccountErrorException(
                    error_msg=_("The used password contains an unaccepted character")
                )
            raise CreateUserAccountErrorException(error_msg=_("Unknown error"))

    return response


def _is_ldap_constraint_email_exists_raised(response):
    return (
        'message' in response.keys()
        and 'Another entry with the same attribute value already exists' in response['message']
        or 'Adresse existante' in response['message']
    )


def _is_email_already_used(response):
    return (
        'message' in response.keys()
        and 'SQL Integrity Error UNIQUE constraint failed: oi_users.email' in response['message']
    )


def _is_ldap_constraint_wrong_password_raised(response):
    return 'message' in response.keys() and 'Value of attribute userpassword contains extended' in response['message']
