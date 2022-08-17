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
from django.shortcuts import render, redirect
from django.utils import translation

from base import settings


def page_not_found(request, exception, **kwargs):
    response = render(request, 'status_page/page_not_found.html', {})
    response.status_code = 404
    return response


def method_not_allowed(request, **kwargs):
    response = render(request, 'status_page/method_not_allowed.html', {})
    response.status_code = 405
    return response


def access_denied(request, exception, **kwargs):
    response = render(request, 'status_page/access_denied.html', {'exception': exception})
    response.status_code = 403
    return response


def server_error(request, **kwargs):
    response = render(request, 'status_page/server_error.html', {})
    response.status_code = 500
    return response


def noscript(request):
    return render(request, 'status_page/noscript.html', {})


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
    response = redirect(request.META['HTTP_REFERER'])
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, translation.get_language())
    return response
