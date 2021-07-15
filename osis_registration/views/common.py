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
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import translation

from osis_registration import settings


def page_not_found(request, exception, **kwargs):
    response = render(request, 'page_not_found.html', {})
    response.status_code = 404
    return response


def method_not_allowed(request, **kwargs):
    response = render(request, 'method_not_allowed.html', {})
    response.status_code = 405
    return response


def access_denied(request, exception, **kwargs):
    response = render(request, 'access_denied.html', {'exception': exception})
    response.status_code = 403
    return response


def server_error(request, **kwargs):
    response = render(request, 'server_error.html', {})
    response.status_code = 500
    return response


def noscript(request):
    return render(request, 'noscript.html', {})


def display_error_messages(request, messages_to_display, extra_tags=None):
    display_messages(request, messages_to_display, messages.ERROR, extra_tags=extra_tags)


def display_success_messages(request, messages_to_display, extra_tags=None):
    display_messages(request, messages_to_display, messages.SUCCESS, extra_tags=extra_tags)


def display_info_messages(request, messages_to_display, extra_tags=None):
    display_messages(request, messages_to_display, messages.INFO, extra_tags=extra_tags)


def display_warning_messages(request, messages_to_display, extra_tags=None):
    display_messages(request, messages_to_display, messages.WARNING, extra_tags=extra_tags)


def display_messages(request, messages_to_display, level, extra_tags=None):
    if not isinstance(messages_to_display, (tuple, list)):
        messages_to_display = [messages_to_display]

    for msg in messages_to_display:
        messages.add_message(request, level, str(msg), extra_tags=extra_tags)


def common_context_processor(request):
    if hasattr(settings, 'ENVIRONMENT'):
        env = settings.ENVIRONMENT
    else:
        env = 'LOCAL'
    context = {
        'installed_apps': settings.INSTALLED_APPS,
        'environment': env,
    }
    return context

def edit_language(request, lang):
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return redirect(request.META['HTTP_REFERER'])
