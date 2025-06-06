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

from django.utils.translation import gettext_lazy as _


class OsisRegistrationServiceException(Exception):
    msg = _("An error occured while using the service: {}")
    error_msg = None

    def __init__(self, error_msg):
        self.error_msg = error_msg
        self.msg = self.msg.format(self.error_msg)
        super().__init__(self.msg)


class RetrieveUserAccountInformationErrorException(OsisRegistrationServiceException):
    msg = _("An error occured while retrieving user account information: {}")


class CreateUserAccountErrorException(OsisRegistrationServiceException):
    msg = _("An error occured while creating user account: {}")

class DeleteUserAccountErrorException(OsisRegistrationServiceException):
    msg = _("An error occured while deleting user account: {}")


class RenewUserAccountValidityErrorException(OsisRegistrationServiceException):
    msg = _("An error occured while renewing user account validity: {}")
