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
from rest_framework import generics
from rest_framework.response import Response

from osis_registration import settings
from osis_registration.models.user_account_creation_request import UserAccountCreationRequest

from rest_framework.authentication import SessionAuthentication


class UserAccountCreationCheck(generics.RetrieveAPIView):
    name = 'user_account_creation_check'
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            account_creation_request = UserAccountCreationRequest.objects.get(uuid=kwargs['uacr_uuid'])
        except UserAccountCreationRequest.DoesNotExist:
            account_creation_request = None

        return Response(
            data={
                "success": account_creation_request.success,
                "ongoing": account_creation_request.attempt <= settings.REQUEST_ATTEMPT_LIMIT
            },
            content_type='application/json'
        )
