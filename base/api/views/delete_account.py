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
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from base.api.serializers.user_account_request import UserAccountRequestSerializer
from base.models.enum import UserAccountRequestType, UserAccountRequestStatus
from base.models.polling_subscriber import PollingSubscriber
from base.models.user_account_request import UserAccountRequest
from base.services.service_exceptions import CreateUserAccountErrorException, \
    RetrieveUserAccountInformationErrorException
from base.services.user_account_deletion import delete_ldap_user_account, SUCCESS
from base.services.user_account_information import get_ldap_user_account_information


class DeleteAccount(generics.DestroyAPIView):
    """
       Delete account request
    """
    name = 'delete-account'
    serializer_class = UserAccountRequestSerializer

    def delete(self, request, *args, **kwargs):
        user_account_deletion_request = None
        user_account_creation_request = None
        try:
            email = request.data['email']

            serializer = self.get_serializer(data={
                "type": UserAccountRequestType.DELETION.name,
                "email": email,
                "subscriber": PollingSubscriber.objects.get(app_name=self.request.user).pk
            })
            serializer.is_valid(raise_exception=True)
            user_account_deletion_request = serializer.save()

            user_account_creation_request = UserAccountRequest.objects.get(
                type=UserAccountRequestType.CREATION.name,
                status=UserAccountRequestStatus.PENDING.name,
                email=email,
            )

            try:
                get_ldap_user_account_information(email=email)
            except RetrieveUserAccountInformationErrorException as e:
                if 'Entry not found' in str(e):
                    user_account_deletion_request.status = UserAccountRequestStatus.ERROR.name
                    user_account_deletion_request.save()
                    user_account_creation_request.status = UserAccountRequestStatus.DELETED.name
                    user_account_creation_request.save()
                raise e

            response = delete_ldap_user_account(user_account_deletion_request)

            if response['status'] == SUCCESS:
                user_account_deletion_request.status = UserAccountRequestStatus.SUCCESS.name
                user_account_deletion_request.save()

                user_account_creation_request.status = UserAccountRequestStatus.DELETED.name
                user_account_creation_request.save()

        except (KeyError, ValueError) as e:
            raise ValidationError(f"Missing data or wrong format: {str(e)}")
        except PollingSubscriber.DoesNotExist:
            return HttpResponseServerError("No matching subscriber")
        except CreateUserAccountErrorException:
            return HttpResponseServerError("An error occured while deleting account")
        except RetrieveUserAccountInformationErrorException as e:
            if user_account_deletion_request:
                user_account_deletion_request.delete()
            return HttpResponseServerError(
                f"An error occured while retrieving account information: {str(e)} -> Request has been updated"
            )


        return HttpResponse(
            status=status.HTTP_200_OK,
            content="Account {} deleted".format(user_account_deletion_request.email)
        )
