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

from osis_registration.forms.registration import RegistrationForm
from osis_registration.override_django_captcha import captcha_audio
from django.utils.translation import LANGUAGE_SESSION_KEY, activate


class RegistrationFormView(FormView):
    name = 'registration'
    template_name = 'home.html'
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        # TODO: move this higher when multiple views avalaible
        # ensure language is loaded from session if any
        if self.request.session[LANGUAGE_SESSION_KEY]:
            activate(self.request.session[LANGUAGE_SESSION_KEY])
        return super(RegistrationFormView, self).dispatch(request, *args, **kwargs)  # Don't forget this

# replace captcha audio with custom captcha audio generator using espeak
views.captcha_audio = captcha_audio