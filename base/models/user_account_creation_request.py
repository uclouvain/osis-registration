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

from django.contrib import admin
from django.db import models

from base.models.polling_subscriber import PollingSubscriber


class UserAccountCreationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'email_validated', 'requested_at', 'attempt', 'success', 'app')
    list_filter = ('success', 'app', 'email_validated')


class UserAccountCreationRequest(models.Model):

    uuid = models.UUIDField(default=uuid_module.uuid4)

    # user data needed to create account
    person_uuid = models.UUIDField(default=uuid_module.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)

    email = models.CharField(max_length=50)
    email_validated = models.BooleanField(default=False)

    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attempt = models.SmallIntegerField(default=0)
    error_payload = models.JSONField(default={})
    app = models.ForeignKey(PollingSubscriber, on_delete=models.CASCADE)

    success = models.BooleanField(default=False)
