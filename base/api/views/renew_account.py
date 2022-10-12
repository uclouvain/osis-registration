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

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.utils.datetime_safe import datetime
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from base.api.serializers.user_account_request import UserAccountRequestSerializer
from base.models.enum import UserAccountRequestType
from base.models.polling_subscriber import PollingSubscriber
from base.services.service_exceptions import RenewUserAccountValidityErrorException
from base.services.user_account_information import get_ldap_user_account_information
from base.services.user_account_renewal import renew_ldap_user_account_validity


class RenewAccount(generics.UpdateAPIView):
    """
       Renew account request
    """
    name = 'renew-account'
    serializer_class = UserAccountRequestSerializer

    def update(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            serializer = self.get_serializer(data={
                "type": UserAccountRequestType.RENEWAL.name,
                "email": email,
                "subscriber": PollingSubscriber.objects.get(app_name=self.request.user).pk
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            account_information = get_ldap_user_account_information(email=email)
            response = renew_ldap_user_account_validity(
                request=request,
                account_id=account_information['id'],
                email=email,
                validity_days=request.data.get('validity_days', settings.LDAP_ACCOUNT_VALIDITY_DAYS)
            )
            new_validity_date = datetime.strptime(response['validite'], '%Y%m%d').strftime('%Y-%m-%d')
            return HttpResponse(
                status=status.HTTP_200_OK,
                content=f"New validity set for {account_information['email']} until {new_validity_date}"
            )

        except (KeyError, ValueError) as e:
            raise ValidationError(f"Missing data or wrong format: {str(e)}")
        except PollingSubscriber.DoesNotExist:
            return HttpResponseServerError("No matching subscriber")
        except RenewUserAccountValidityErrorException as e:
            return HttpResponseServerError(e.msg)

