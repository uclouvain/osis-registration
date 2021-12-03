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
from django.contrib import admin, auth

from base.messaging import message_history, message_template
from base.models.polling_subscriber import PollingSubscriber, PollingSubscriberAdmin
from base.models.user import OsisRegistrationUserAdmin
from base.models.user_account_creation_request import UserAccountCreationRequest, UserAccountCreationRequestAdmin

admin.site.register(
    message_history.MessageHistory,
    message_history.MessageHistoryAdmin,
)

admin.site.register(
    message_template.MessageTemplate,
    message_template.MessageTemplateAdmin,
)

admin.site.register(
    PollingSubscriber,
    PollingSubscriberAdmin,
)

admin.site.register(
    UserAccountCreationRequest,
    UserAccountCreationRequestAdmin
)

# replace user admin with custom admin
User = auth.get_user_model()
admin.site.unregister(User)
admin.site.register(User, OsisRegistrationUserAdmin)
