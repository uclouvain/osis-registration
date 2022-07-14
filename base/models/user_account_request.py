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

import uuid

from django.contrib import admin
from django.db import models

from base.models.enum import UserAccountRequestType, UserAccountRequestStatus


class UserAccountRequestAdmin(admin.ModelAdmin):
    fields = ('email', 'email_validated', 'type', 'status')
    list_display = ('uuid', 'email', 'email_validated', 'type', 'status')


class UserAccountRequest(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField()
    email_validated = models.BooleanField(default=False)
    type = models.CharField(choices=UserAccountRequestType.choices(), max_length=50)

    status = models.CharField(
        choices=UserAccountRequestStatus.choices(),
        default=UserAccountRequestStatus.PENDING.value,
        max_length=50
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
