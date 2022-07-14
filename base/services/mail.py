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
from django.shortcuts import reverse

from base.messaging import send_message, message_config
from base.services.token_generator import mail_validation_token_generator


def send_email(template_references, receivers, data, connected_user=None):
    message_content = message_config.create_message_content(
        template_references['html'],
        template_references['txt'],
        [],
        receivers,
        data['template'],
        data['subject'],
        data.get('attachment')
    )
    send_message.send_messages(
        message_content=message_content,
        connected_user=connected_user
    )

def send_validation_mail(request, user_account_creation_request):
    template_references = {
        'html': 'osis_registration_mail_validation_html',
        'txt': 'osis_registration_mail_validation_txt'
    }
    # TODO: change receiver_person_id
    receivers = [
        message_config.create_receiver(
            receiver_email=user_account_creation_request.request.email,
            receiver_lang=None
        )
    ]
    token = mail_validation_token_generator.make_token(user_account_creation_request)
    data = {
        'template': {'link': request.build_absolute_uri(reverse('validate_email', kwargs={
            'uacr_uuid': user_account_creation_request.request.uuid,
            'token': token
        }))},
        'subject': {}
    }
    send_email(template_references, receivers, data)
