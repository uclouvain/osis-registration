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

from django.conf import settings
from django.http import JsonResponse
from django.utils.datetime_safe import datetime
from rest_framework import generics

from base.models.polling_subscriber import PollingSubscriber
from base.services.service_exceptions import RenewUserAccountValidityErrorException
from base.services.user_account_information import get_ldap_user_account_information
from base.services.user_account_renewal import renew_ldap_user_account_validity


class RenewAccount(generics.UpdateAPIView):
    """
       Renew account request
    """
    name = 'renew-account'

    def update(self, request, *args, **kwargs):
        try:
            PollingSubscriber.objects.get(app_name=self.request.user)
            account_information = get_ldap_user_account_information(email=request.data['email'])
            response = renew_ldap_user_account_validity(
                account_id=account_information['id'],
                email=request.data['email'],
                validity_days=request.data.get('validity_days', settings.LDAP_ACCOUNT_VALIDITY_DAYS)
            )
            new_validity_date = datetime.strptime(response.json()['validite'], '%Y%m%d').strftime('%Y-%m-%d')
            return JsonResponse(data={
                "status": "SUCCESS",
                "msg": f"New validity set for {account_information['email']} until {new_validity_date}"
            })
        except PollingSubscriber.DoesNotExist:
            return JsonResponse(data={"status": "ERROR", "msg": "No matching subscriber"})
        except RenewUserAccountValidityErrorException as e:
            return JsonResponse(data={"status": "ERROR", "msg": e.msg})
