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
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.utils.datetime_safe import datetime
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from base.api.serializers.user_account_request import UserAccountRequestSerializer
from base.models.enum import UserAccountRequestType
from base.models.polling_subscriber import PollingSubscriber
from base.services import mail
from base.services.service_exceptions import CreateUserAccountErrorException
from base.services.user_account_creation import create_ldap_user_account, SUCCESS
from base.views.registration import UserAccountCreationRequest


class CreateAccount(generics.CreateAPIView):
    """
       Create account request
    """
    name = 'create-account'
    serializer_class = UserAccountRequestSerializer

    def create(self, request, *args, **kwargs):
        try:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            birth_date = datetime.strptime(request.data['birth_date'], '%Y-%m-%d')
            email = request.data['email']
            password = request.data['password']
            serializer = self.get_serializer(data={
                "type": UserAccountRequestType.CREATION.name,
                "email": email,
                "subscriber": PollingSubscriber.objects.get(app_name=self.request.user).pk
            })
            serializer.is_valid(raise_exception=True)
            user_account_request = serializer.save()

            user_account_creation_request = UserAccountCreationRequest(
                request=user_account_request,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                password=password,
            )

            ldap_response = create_ldap_user_account(user_account_creation_request)
            if ldap_response.get('status') == SUCCESS:
                mail.send_validation_mail(self.request, user_account_creation_request)

        except (KeyError, ValueError) as e:
            raise ValidationError(f"Missing data or wrong format: {str(e)}")
        except PollingSubscriber.DoesNotExist:
            return HttpResponseServerError("No matching subscriber")
        except CreateUserAccountErrorException:
            return HttpResponseServerError("An error occured while creating account")

        return HttpResponse(
            status=status.HTTP_201_CREATED,
            content="Account {} created: please validate email by following the link received".format(user_account_request.email)
        )
