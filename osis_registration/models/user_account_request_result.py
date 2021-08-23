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

import uuid as uuid_module
from django.db import models

from osis_registration.models.user_account_creation_request import UserAccountCreationRequest
from osis_registration.models.user_account_deletion_request import UserAccountDeletionRequest
from osis_registration.models.user_account_renewal_request import UserAccountRenewalRequest

SUCCESS = 'SUCCESS'
ERROR = 'ERROR'

class UserAccountRequestResult(models.Model):

    uuid = models.UUIDField(default=uuid_module.uuid4)

    person_uuid =  models.UUIDField(null=True)
    request_type = models.CharField(
        max_length=50,
        choices=[
            (UserAccountCreationRequest,'CREATION'),
            (UserAccountDeletionRequest,'DELETION'),
            (UserAccountRenewalRequest,'RENEWAL')
        ]
    )
    status = models.CharField(
        max_length=7,
        choices=[
            (SUCCESS, SUCCESS),
            (ERROR, ERROR)
        ]
    )
