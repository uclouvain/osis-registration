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
from captcha import views
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from osis_registration.forms.registration import RegistrationForm
from osis_registration.override_django_captcha import captcha_audio


class RegistrationFormView(FormView):
    name = 'registration'
    template_name = 'home.html'
    success_url = '/registration_success'
    form_class = RegistrationForm


# replace captcha audio with custom captcha audio generator using espeak
views.captcha_audio = captcha_audio


class RegistrationSuccessView(TemplateView):
    name = 'registration_success'
    template_name = 'registration_success.html'
