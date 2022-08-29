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
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.http.response import JsonResponse
from django.utils.datetime_safe import datetime
from rest_framework import generics

from base.api.serializers.user_account_request import UserAccountRequestSerializer
from base.services.service_exceptions import CreateUserAccountErrorException
from base.services.user_account_creation import create_ldap_user_account
from base.views.registration import UserAccountCreationRequest


class CreateAccount(generics.CreateAPIView):
    """
       Create account request
    """
    name = 'create-account'
    serializer_class = UserAccountRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        try:
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            birth_date = self.request.POST['birth_date']
        except KeyError as e:
            return HttpResponseBadRequest("Missing data or wrong format: " + str(e))

        user_account_creation_request = UserAccountCreationRequest(
            request=serializer,
            first_name=first_name,
            last_name=last_name,
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d'),
        )

        try:
            create_ldap_user_account(user_account_creation_request)
        except CreateUserAccountErrorException:
            return HttpResponseServerError("An error occured while creating account")

        return JsonResponse(data={"status": "Success", "message": "Account {} created".format(serializer.email)})
