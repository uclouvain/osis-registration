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

import secrets

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OsisRegistrationUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['password1'].required = False
        self.base_fields['password2'].required = False
        super().__init__(*args, **kwargs)

    def clean(self):
        password = secrets.token_hex()
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password
        return super().clean()

class OsisRegistrationUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username',)
        }),
    )
    form = OsisRegistrationUserCreationForm
    add_form = OsisRegistrationUserCreationForm


def get_osis_registration_user():
    return User.objects.get(username='osis_registration')
