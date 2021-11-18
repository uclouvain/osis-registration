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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import datetime
from unittest import mock
from captcha import views
from captcha.models import CaptchaStore

from django.test import TestCase, RequestFactory
from django.http.response import Http404
from base.views import registration

class OverrideDjangoCaptchaTestCase(TestCase):

    def setUp(self) -> None:
        CaptchaStore.objects.create(
            challenge="challenge",
            response="response",
            hashkey="key",
            expiration=datetime.datetime.now()
        )

    @mock.patch('os.remove')
    @mock.patch('os.rename')
    @mock.patch('subprocess.call')
    def test_should_override_captcha_audio_to_use_espeak_and_sox(self, mock_subprocess, mock_file_rename, mock_file_remove):
        request = RequestFactory().get('/')
        with self.assertRaises(Http404):
            views.captcha_audio(request, 'key')

        for cli_util in ['espeak', 'sox']:
            self.assertTrue(f"/usr/bin/{cli_util}" in str(mock_subprocess.call_args_list))
