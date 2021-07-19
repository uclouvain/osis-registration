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
import logging

from osis_registration import settings
from osis_registration.celery import app as celery_app
from osis_registration.models import UserAccountCreationRequest
from osis_registration.services import request_result
from osis_registration.services.user_account_creation import create_ldap_user_account, SUCCESS

logger = logging.getLogger(settings.DEFAULT_LOGGER)

class TooManyCreationRequestAttemptsException(Exception):
    pass


@celery_app.task
def run() -> dict:
    """
    This job will get user creation requests stored in db and create users via ldap user creation endpoint.
    """

    too_many_attempts_requests = []
    resulted_requests = []

    pending_creation_requests = UserAccountCreationRequest.objects.filter(
        success=False,
        attempt__lte=settings.REQUEST_ATTEMPT_LIMIT
    )

    for user_creation_request in pending_creation_requests:
        response = create_ldap_user_account(user_creation_request)
        if response['status'] == SUCCESS:
            user_creation_request.success = True
            user_creation_request.attempt += 1
            user_creation_request.save()

            resulted_requests.append(user_creation_request)
            logger.info('User created : {}'.format(user_creation_request.email))
        else:
            user_creation_request.error_payload.update(
                {
                   'error_{}'.format(user_creation_request.attempt): response['message']
                }
            )
            user_creation_request.attempt += 1
            user_creation_request.save()

            if user_creation_request.attempt > settings.REQUEST_ATTEMPT_LIMIT:
                too_many_attempts_requests.append(user_creation_request)
                resulted_requests.append(user_creation_request)

            logger.info('Error - user not created : {}'.format(user_creation_request.email))

    if too_many_attempts_requests:
        raise TooManyCreationRequestAttemptsException()

    request_result.store(resulted_requests)

    return {}
