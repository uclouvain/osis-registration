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

from django.db import models


class UserAccountCreationRequest(models.Model):

    # user data needed to create account
    person_uuid =  models.UUIDField(default=uuid.uuid4())
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attempt = models.SmallIntegerField(default=0)
    error_payload = models.JSONField(default={})
    app_name = models.CharField(max_length=50)

    account_created = models.BooleanField(default=False)


class UserAccountDeletionRequest(models.Model):

    # user data needed to delete account
    person_uuid =  models.UUIDField(default=uuid.uuid4())
    email = models.CharField(max_length=50)

    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attempt = models.SmallIntegerField(default=0)
    error_payload = models.JSONField(default={})
    app_name = models.CharField(max_length=50)

    account_deleted = models.BooleanField(default=False)


class UserAccountRenewalRequest(models.Model):

    # user data needed to renew account
    person_uuid =  models.UUIDField(default=uuid.uuid4())
    email = models.CharField(max_length=50)

    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attempt = models.SmallIntegerField(default=0)
    error_payload = models.JSONField(default={})
    app_name = models.CharField(max_length=50)

    account_renewed = models.BooleanField(default=False)


class UserAccountRequestResult(models.Model):

    person_uuid =  models.UUIDField()
    request_type = models.CharField(
        max_length=9,
        choices=[
            ('CREATION','CREATION'),
            ('DELETION','DELETION'),
            ('RENEWAL','RENEWAL')
        ]
    )
    status = models.CharField(
        max_length=7,
        choices=[
            ('SUCCESS','SUCCESS'),
            ('ERROR','ERROR')
        ]
    )
