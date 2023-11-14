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
from django.urls import path

from base.api.views.acknowledge_poll import AcknowledgePoll
from base.api.views.create_account import CreateAccount
from base.api.views.delete_account import DeleteAccount
from base.api.views.renew_account import RenewAccount

urlpatterns = [
    path('create_account/', CreateAccount.as_view(), name=CreateAccount.name),
    path('delete_account/', DeleteAccount.as_view(), name=DeleteAccount.name),
    path('renew_account/', RenewAccount.as_view(), name=RenewAccount.name),
    path('acknowledge/', AcknowledgePoll.as_view(), name=AcknowledgePoll.name),
]
