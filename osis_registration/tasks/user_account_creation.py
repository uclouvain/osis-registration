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
from osis_registration.services.user_account_creation import create_ldap_user_account, SUCCESS

from django.db.models import F

logger = logging.getLogger(settings.DEFAULT_LOGGER)


@celery_app.task
def run() -> dict:
    """
    This job will get user creation requests stored in db and create users via ldap user creation endpoint.
    """

    pending_creation_requests = UserAccountCreationRequest.objects.filter(account_created=False, retry__lte=3)

    for user_creation_request in pending_creation_requests:
        response = create_ldap_user_account(user_creation_request)
        if response['status'] == SUCCESS:
            user_creation_request.account_created = True
            user_creation_request.save()
            logger.info('User created : {}'.format(user_creation_request.email))
        else:
            logger.info('Error - user not created : {}'.format(user_creation_request.email))

    pending_creation_requests.update(retry=F('retry') + 1)

    return {}